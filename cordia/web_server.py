from aiohttp import web
from discord import Embed
import discord
from cordia.cordia_client import CordiaClient
from cordia.model.item_instance import ItemInstance


class WebServer:
    def __init__(self, cordia_client: CordiaClient, topgg_auth_token: str):
        self.cordia_client = cordia_client
        self.topgg_auth_token = topgg_auth_token
        self.app = web.Application(middlewares=[self.error_middleware])
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_post("/webhook/topgg", self.handle_topgg_vote)
        # Add a catch-all route for 404s
        self.app.router.add_route("*", "/{path:.*}", self.handle_404)

    @web.middleware
    async def error_middleware(self, request, handler):
        try:
            response = await handler(request)
            return response
        except Exception as e:
            import traceback
            # Don't log expected Discord API errors as errors
            if "Not Found" in str(e) or "Forbidden" in str(e):
                self.cordia_client.logger.debug(f"Expected Discord API error in web server: {e}")
            elif "404" in str(e):
                self.cordia_client.logger.debug(f"404 error in web server: {e}")
            else:
                self.cordia_client.logger.error(f"Unhandled exception in web server: {e}")
                self.cordia_client.logger.debug(f"Traceback: {traceback.format_exc()}")
            return web.Response(status=500, text="Internal server error")

    async def handle_topgg_vote(self, request):
        self.cordia_client.logger.info("Handling vote")
        # Validate Authorization
        auth = request.headers.get("Authorization")
        if auth != self.topgg_auth_token:
            self.cordia_client.logger.warning(f"Unauthorized webhook request from {request.remote}")
            return web.Response(status=401, text="Unauthorized")

        # Parse JSON Payload
        try:
            data = await request.json()
            discord_id = int(data.get("user"))
            if not discord_id:
                self.cordia_client.logger.warning("Invalid webhook data format - missing user ID")
                return web.Response(status=400, text="Invalid data format")

            # Process the Vote
            reward_item, reward_count = (
                await self.cordia_client.cordia_service.vote_service.give_vote_reward(
                    discord_id
                )
            )
            item_instance = ItemInstance(0, reward_item, reward_count, None, None)
            self.cordia_client.logger.info(f"Vote received for user: {discord_id}")

            # Notify the User
            try:
                self.cordia_client.logger.debug(f"Attempting to fetch user {discord_id} for vote notification")
                user = await self.cordia_client.fetch_user(discord_id)
                if user:
                    try:
                        embed = Embed(
                            title="🎉 Thank You for Voting!",
                            description=f"You've been rewarded for supporting Cordia!",
                            color=discord.Color.green(),  # Green color
                        )
                        embed.add_field(
                            name="Reward",
                            value=item_instance.display_item(),
                            inline=False,
                        )
                        embed.set_footer(
                            text="Your support helps make Cordia even better!"
                        )
                        await user.send(embed=embed)
                    except discord.Forbidden:
                        # User has DMs disabled
                        self.cordia_client.logger.debug(f"User {discord_id} has DMs disabled")
                    except discord.NotFound:
                        # User no longer exists
                        self.cordia_client.logger.debug(f"User {discord_id} not found in Discord")
                    except Exception as e:
                        self.cordia_client.logger.warning(
                            f"Failed to DM user {discord_id}: {e}"
                        )
            except discord.NotFound:
                # User no longer exists
                self.cordia_client.logger.debug(f"User {discord_id} not found in Discord")
            except discord.Forbidden:
                # Bot can't access user
                self.cordia_client.logger.debug(f"Cannot access user {discord_id} (forbidden)")
            except Exception as e:
                # Other errors - log but don't fail the webhook
                self.cordia_client.logger.debug(f"Failed to fetch user {discord_id}: {e}")

            return web.Response(status=200, text="Vote processed successfully")

        except Exception as e:
            self.cordia_client.logger.error(f"Error handling webhook: {e}")
            return web.Response(status=500, text="Internal server error")

    async def handle_404(self, request):
        """Handle 404 requests to prevent them from being logged as errors."""
        self.cordia_client.logger.debug(f"404 Not Found: {request.method} {request.path} from {request.remote}")
        return web.Response(status=404, text="Not Found")

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        self.cordia_client.logger.info("Web server started on http://0.0.0.0:8080")
