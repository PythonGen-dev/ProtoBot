from discord.ext import commands
import discord
try:
	from modules import getcolorfromurl, storage, getlang, getcustomemote
	translates = storage("./locals/langs.lang")
	emotes = storage("./locals/emotes.lang")
except: pass
import re
import random


class Board:
    def __init__(self, player1, player2):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

        if random.SystemRandom().randint(0, 1):
            self.challengers = {"x": player1, "o": player2}
        else:
            self.challengers = {"x": player2, "o": player1}

        self.X_turn = True

    def full(self):

        for row in self.board:
            if " " in row:
                return False
        return True

    def can_play(self, player):
        if self.X_turn:
            return player == self.challengers["x"]
        else:
            return player == self.challengers["o"]

    def update(self, x, y):
        letter = "x" if self.X_turn else "o"
        if self.board[x][y] == " ":
            self.board[x][y] = letter
        else:
            return False
        self.X_turn = not self.X_turn
        return True

    def check(self):
        if (
            self.board[0][0] == self.board[0][1]
            and self.board[0][0] == self.board[0][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        if (
            self.board[0][0] == self.board[1][0]
            and self.board[0][0] == self.board[2][0]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        if (
            self.board[0][0] == self.board[1][1]
            and self.board[0][0] == self.board[2][2]
            and self.board[0][0] != " "
        ):
            return self.challengers[self.board[0][0]]
        if (
            self.board[0][2] == self.board[1][2]
            and self.board[0][2] == self.board[2][2]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]
        if (
            self.board[0][2] == self.board[1][1]
            and self.board[0][2] == self.board[2][0]
            and self.board[0][2] != " "
        ):
            return self.challengers[self.board[0][2]]
        if (
            self.board[2][2] == self.board[2][1]
            and self.board[2][2] == self.board[2][0]
            and self.board[2][2] != " "
        ):
            return self.challengers[self.board[2][2]]
        if (
            self.board[1][1] == self.board[0][1]
            and self.board[1][1] == self.board[2][1]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]
        if (
            self.board[1][1] == self.board[1][0]
            and self.board[1][1] == self.board[1][2]
            and self.board[1][1] != " "
        ):
            return self.challengers[self.board[1][1]]
            
        return None

    def __str__(self):
        
        _board = "{}{}{}\n".format(self.board[0][0], self.board[0][1], self.board[0][2])
        _board += "{}{}{}\n".format(self.board[1][0], self.board[1][1], self.board[1][2])
        _board += "{}{}{}".format(self.board[2][0], self.board[2][1], self.board[2][2])
        _board = _board.replace(" ", emotes.get("empty"))
        _board = _board.replace("x", emotes.get("tttx"))
        _board = _board.replace("o", emotes.get("ttto"))
        return "{}".format(_board)


class TicTacToe(commands.Cog):

    boards = {}

    def create(self, server_id, player1, player2):
        self.boards[server_id] = Board(player1, player2)

        return self.boards[server_id].challengers["x"]

    @commands.group(aliases=["tic", "tac", "toe"], invoke_without_command=True, name = "ttt")
    @commands.guild_only()
    async def tictactoe(self, ctx, *, option: str = None):
        guildlang = getlang(ctx)
        if option == None:
            await ctx.send(embed=discord.Embed(title=translates.get('ErrNotArg' + guildlang)))
            return
        
        player = ctx.message.author
        board = self.boards.get(ctx.message.guild.id)
        if not board:
            await ctx.send(embed = discord.Embed(title=translates.get('notttgamesstarted' + guildlang)))
            return
        if not board.can_play(player):
            await ctx.send(embed = discord.Embed(title=translates.get('cantplaynowttt' + guildlang)))
            return
            
        topleft = re.search("1", option)    
        top = re.search("2", option)
        topright = re.search("3", option)
        left = re.search("4", option)
        middle = re.search("5", option)        
        right = re.search("6", option)        
        bottom = re.search("8", option)
        bottomleft = re.search("7", option)
        bottomright = re.search("9", option)
        
        if not top and not bottom and not left and not right and not middle and not topleft and not topright and not bottomleft and not bottomright:
            await ctx.send(embed = discord.Embed(title=translates.get('selectvalidcagettt' + guildlang)))
            return

        x = 0
        y = 0
        
        if top:
            x = 0
            y = 1
        elif bottom:
            x = 2
            y = 1
        elif middle:
        	x = 1
        	y = 1
        elif left:
            y = 0
            x = 1
        elif right:
            y = 2
            x = 1
        elif topleft:
        	x = 0
        	y = 0
        elif topright:
        	x = 0
        	y = 2
        elif bottomleft:
        	x = 2
        	y = 0
        elif bottomright:
        	x = 2
        	y = 2
        	

        if not board.update(x, y):
            await ctx.send(embed = discord.Embed(title=translates.get('someonealreadyplayedherettt' + guildlang)))
            return
        
        winner = board.check()
        if winner:
            await ctx.send(embed = discord.Embed(title=str(winner.display_name)+" "+translates.get('playerwinttt' + guildlang)))
  
           
            try:
                del self.boards[ctx.message.guild.id]
            except KeyError:
                pass
        else:
            if board.full():
                await ctx.send(embed = discord.Embed(title=translates.get('tieendttt' + guildlang)))
                try:
                    del self.boards[ctx.message.guild.id]
                except KeyError:
                    pass
            else:
                player_turn = (
                    board.challengers.get("x")
                    if board.X_turn
                    else board.challengers.get("o")
                )
                embed = discord.Embed(title=translates.get('Tic-Tac-Toe' + guildlang), description = str(board)).set_author(name = str(player_turn.display_name), icon_url = player_turn.avatar_url)
                await ctx.send(embed = embed)

    @tictactoe.command(name="start")
    @commands.guild_only()
    async def start_game(self, ctx, player2: discord.Member = None):
        guildlang = getlang(ctx)
        player1 = ctx.message.author
        if player2 == None:
            await ctx.send(embed = discord.Embed(title=translates.get('cantplaywithselfbotttt' + guildlang)))
            return
        if self.boards.get(ctx.message.guild.id) is not None:
            await ctx.send(embed = discord.Embed(title=translates.get('onlyonetttatserverr' + guildlang)))
            return
        if player2 == ctx.message.guild.me:
            await ctx.send(embed = discord.Embed(title=translates.get('cantplaywithselfbotttt' + guildlang)))
            return
        if player2 == player1:
            await ctx.send(embed = discord.Embed(title=translates.get('cantplaywithyourselfttt' + guildlang)))
            return
        if player2.bot == True:
            await ctx.send(embed = discord.Embed(title=translates.get('infoAboutBotErr' + guildlang)))
            return

        
        x_player = self.create(ctx.message.guild.id, player1, player2)
        embed = discord.Embed(title=translates.get('Tic-Tac-Toe' + guildlang), description = str(self.boards[ctx.message.guild.id])).set_author(name = str(x_player.display_name), icon_url = x_player.avatar_url)
        await ctx.send(embed = embed)
        

def setup(bot):
    bot.add_cog(TicTacToe(bot))
