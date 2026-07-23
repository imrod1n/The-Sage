import config
import logger



def setup_commands(tree, user_context):

    @tree.command(name="help", description="Список команд")
    async def help_command(interaction):
        await interaction.response.send_message(config.BOT_HELP_TEXT)


    @tree.command(name="reset", description="Очистить память")
    async def reset_command(interaction):
        user_context.pop(interaction.user.id, None)
        await interaction.response.send_message(config.CONTEXT_RESET_MESSAGE)