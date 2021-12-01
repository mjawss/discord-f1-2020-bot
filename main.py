import discord
import csv

DRIVERS_HEADER = ['Name','Full Name','Points','Constructor']
CONSTRUCTORS_HEADER = ['Constructor', 'Points']
CONSTRUCTORS = [
    "Mercedes", 
    "Ferrari", 
    "Red_Bull",
    "Mclaren",
    "Haas",
    "Alfa_Romeo",
    "AlphaTauri",
    "Renault",
    "Aston_Martin",
    "Williams"
]
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Mazespin out of existence"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    
    if msg.startswith('$help'):
        string = "The commands you can use are:\n$drivers: Shows the current driver standings.\n$constructors: Shows the current constructor standings."
        await message.channel.send(string)
        return

    if msg.startswith('$add_driver'):
        check_role = discord.utils.get(message.author.roles, name="Bernie")
        if check_role != None:
            info = msg.split(" ")
            if len(info) != 4:
                await message.channel.send("Please use the command as: $add_driver NAM Full_Name Constructor")
                return
            
            d_name = info[1]
            d_fname = info[2]
            d_con = info[3]
            new_line = [d_name, d_fname, "0", d_con]

            if len(d_name) != 3:
                await message.channel.send("Please use the command as: $add_driver NAM Full_Name Constructor")
                return
        
            if len(d_name.split()) != 1 or len(d_fname.split()) != 1 or len(d_con.split()) != 1:
                await message.channel.send("Please use the command as: $add_driver NAM Full_Name Constructor")
                return
            
            if d_con not in CONSTRUCTORS:
                await message.channel.send("Please specify a valid constructor: {}".format(CONSTRUCTORS))
                return

            with open('f1drivers.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                to_sort = (list(csv_reader))[1:]
                sortedLs = sorted(to_sort, key=lambda row: int(row[2]), reverse=True)
                csv_file.close()  

                count = 0
                for line in sortedLs:
                    if d_con in line:
                        count += 1
                    if d_name in line and d_fname in line:
                        await message.channel.send("This driver already exists!")
                        return
                if count == 2:
                    await message.channel.send("{} is currently full, please choose another constructor!".format(d_con))
                    return
                sortedLs.append(new_line) 

            with open('f1drivers.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(DRIVERS_HEADER)
                for line in sortedLs:
                    csv_writer.writerow(line)
                csv_file.close()
                await message.channel.send("{} has been successfully added to the driver lineup!".format(d_name))
        else:
            await message.channel.send("You do not have permission to use this command!")
            
    if msg.startswith('$drivers'):
        with open('f1drivers.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            to_sort = (list(csv_reader))[1:]
            sortedLs = sorted(to_sort, key=lambda row: int(row[2]), reverse=True)
            i = 1
            string = "The current driver standings are as follows:\n"
            for driver in sortedLs:
                name = driver[0]
                points = driver[2]
                add = "{}. Name: {}, Points: {}\n".format(i, name, points)
                string += add
                i += 1
            await message.channel.send(string)
        csv_file.close()   

    if msg.startswith('$constructors'):
        with open('f1constructors.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            to_sort = (list(csv_reader))[1:]
            sortedLs = sorted(to_sort, key=lambda row: int(row[1]), reverse=True)
            string = "The current driver standings are as follows:\n"
            i = 1
            for constructor in sortedLs:
                name = constructor[0]
                points = constructor[1]
                add = "{}. {}, Points: {}\n".format(i, name, points)
                string += add
                i += 1
            await message.channel.send(string)
        csv_file.close()   

    if msg.startswith('$update'):
        check_role = discord.utils.get(message.author.roles, name="Bernie")
        if check_role != None:
            info = msg.split(" ")
            if len(info) != 3:
                await message.channel.send("Please use the command as: $update NAM Points")
                return
            
            d_name = info[1]
            d_points = info[2]

            if len(d_name) != 3:
                await message.channel.send("Please use the command as: $add_driver NAM Full_Name Constructor")
                return
            
            try:
                d_points = int(d_points)
                if d_points > 26 or d_points < 0:
                    raise Exception
            except Exception:
                await message.channel.send("Please enter a valid number [0-26].")
                return
            
            with open('f1drivers.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                ls = list(csv_reader)[1:]
                csv_file.close()
                cons = ""
                for line in ls:
                    l_name = line[0]
                    if d_name == l_name:
                        line[2] = str(int(line[2])+d_points)
                        cons = line[3]
                        break

            with open('f1drivers.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(DRIVERS_HEADER)
                for line in ls:
                    csv_writer.writerow(line)
                csv_file.close()
                await message.channel.send("{} has been awarded {} points!".format(d_name, d_points))

            with open('f1constructors.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                ls = list(csv_reader)[1:]
                csv_file.close()
                for line in ls:
                    l_cons = line[0]
                    if cons == l_cons:
                        line[1] = str(int(line[1])+d_points)
                        break

            with open('f1constructors.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(CONSTRUCTORS_HEADER)
                for line in ls:
                    csv_writer.writerow(line)
                csv_file.close()
                await message.channel.send("{} has been awarded {} points!".format(cons, d_points)) 
        else:
            await message.channel.send("You do not have permission to use this command!")

client.run('ODQ3MzYyNjY3NjE3MzIwOTkx.YK89-w.HXSa5yM_uJ169_NBTH8mpCvEojw')