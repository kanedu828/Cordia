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

    @web.middleware
    async def error_middleware(self, request, handler):
        try:
            response = await handler(request)
            return response
        except Exception as e:
            self.cordia_client.logger.error(f"Unhandled exception: {e}")
            return web.Response(status=500, text="Internal server error")

    async def handle_topgg_vote(self, request):
        # Validate Authorization
        auth = request.headers.get("Authorization")
        if auth != self.topgg_auth_token:
            return web.Response(status=401, text="Unauthorized")

        # Parse JSON Payload
        try:
            data = await request.json()
            discord_id = int(data.get("user"))
            if not discord_id:
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
                user = await self.cordia_client.fetch_user(discord_id)
                if user:
                    try:
                        embed = Embed(
                            title="🎉 Thank You for Voting!",
                            description=f"You've been rewarded for supporting Cordia!",
                            color=discord.Color.green(),  # Green color
                        )
                        embed.add_field(
                            name="Reward", value=item_instance.display_item(), inline=False
                        )
                        embed.set_footer(text="Your support helps make Cordia even better!")
                        await user.send(embed=embed)
                    except Exception as e:
                        self.cordia_client.logger.warning(
                            f"Failed to DM user {discord_id}: {e}"
                        )
            except:
                # Prevent spam in logs for no user
                pass

            return web.Response(status=200, text="Vote processed successfully")

        except Exception as e:
            self.cordia_client.logger.error(f"Error handling webhook: {e}")
            return web.Response(status=500, text="Internal server error")

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()
        self.cordia_client.logger.info("Web server started on http://0.0.0.0:8080")
