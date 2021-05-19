import asyncpg
import asyncio

databaseurl=""

def createtableconvertlist(data: list):
    toreturn = str()
    for sec in data:
        toreturn+=str(sec[0])+" "+str(sec[1])+", "
    toreturn = toreturn[:-2]
    return toreturn

def insertrowconvertlist(data: list):
    toreturn = "("
    for sec in data: toreturn+=str(sec[0])+", "
    toreturn=toreturn[:-2]+") VALUES("
    for sec in data: toreturn+=str(sec[1])+", "
    toreturn=toreturn[:-2]+")"
    return toreturn


def orderdataconvertlist(data: list):
    toreturn = str()
    for sec in data: toreturn += str(sec[0])+" "+str(sec[1])+" AND "
    toreturn = toreturn [:-5]
    return toreturn


def wheredataconvertlist(data: list):
    toreturn = str()
    for sec in data: toreturn += str(sec[0])+" = "+str(sec[1])+" AND "
    toreturn = toreturn [:-5]
    return toreturn

def setdataconvertlist(data: list):
    toreturn = str()
    for sec in data: toreturn+=str(sec [0])+" = "+str(sec[1])+", "
    toreturn = toreturn[:-2]
    return toreturn

async def aioconnect():
    conn = await asyncpg.connect(databaseurl)
    return conn
    
async def aiocreatetable(tablename: str, cols: list):
    #пример для cols: data = [["guildid", "text"], ["userid", "text"], ["value", "text"]]
    conn = await aioconnect()
    await conn.execute(f'''CREATE TABLE {tablename}({createtableconvertlist(cols)})''')
    await conn.close()
    
async def aioinsertrow(tablename: str, rowdata: list):
    #пример для rowdata: data = [["guildid", 11000], ["userid", 7737383], ["value", 1]]
    conn = await aioconnect()
    await conn.execute(f'''INSERT INTO {tablename}{insertrowconvertlist(rowdata)}''')
    await conn.close()

async def aioupdaterow(tablename: str, newdata: list, wheredata: list):
    #wheredata = [["guildid", 11000],["userid", 7737383]]
    #newdata = [["value", 2822], ["userid", 828282]]
    conn = await aioconnect()
    await conn.execute(f"""UPDATE {tablename} SET {setdataconvertlist(newdata)} WHERE {wheredataconvertlist(wheredata)}""")
    await conn.close()
    
async def aiogetrow(tablename: str, wheredata: list):
    conn = await aioconnect()
    row = await conn.fetchrow(f'SELECT * FROM {tablename} WHERE {wheredataconvertlist(wheredata)}')
    await conn.close() 
    return row
    
async def aioupsertrow(tablename: str, newdata: list, wheredata: list):
    oldrow = await aiogetrow(tablename, wheredata)
    if oldrow is None:
        await aioinsertrow(tablename, newdata)
    else:
        await aioupdaterow(tablename, newdata, wheredata)

async def aioorderfetch(tablename: str, wheredata: list, orderdata: list):
    conn = await aioconnect()
    rows = await conn.fetch(f'SELECT * FROM {tablename} WHERE {wheredataconvertlist(wheredata)} order by {orderdataconvertlist(orderdata)}')
    await conn.close() 
    return rows
