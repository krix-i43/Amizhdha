import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
import asyncio
import signal
import sys
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

#-----------------Globals-------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
insquad = None 
joining_team = False
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
reject_spam_task = None
lag_running = False
lag_task = None
fun_group_running = False
fun_group_task = None
fun_rspam_running = False
fun_rspam_task = None
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
evo_cycle_task = None
ADMIN_UID ={"122809569" , "1743892056"}
#---------------------Emote Command---------------------#
evo_emotes = {
    "1": "909000063",   # Ak
    "2": "909000068",   # Scar
    "3": "909000075",   # 1st MP40
    "4": "909000081",   # 1st M1014
    "5": "909000085",   # XM8
    "6": "909000098",   # UMP
    "7": "909000090",   # Famas
    "8": "909033002",   # MP5
    "9": "909035007",   # M1887
    "10": "909033001",  # M4A1
    "11": "909037011",  # Fist
    "12": "909035012",  # AN94
    "13": "909038010",  # Thompson
    "14": "909039011",   # 2nd M1014
    "15": "909040010",   # 2nd MP40
    "16": "909041005",  # Groza
    "17": "909042008",  # Woodpecker
    "18": "909045001",  # Parafal
    "19": "909049010",  # P90
    "20": "909038012",  # G18
    "21": "909051003"   # M60
}
#--------------Emote mapping for evo commands---------#
EMOTE_MAP = {
    1: 909000063,
    2: 909000068,
    3: 909000075,
    4: 909000081,
    5: 909000085,
    6: 909000098,
    7: 909000090,
    8: 909033002,
    9: 909035007,
    10: 909033001,
    11: 909037011,
    12: 909035012,
    13: 909038010,
    14: 909039011,
    15: 909040010,
    16: 909041005,
    17: 909042008,
    18: 909045001,
    19: 909049010,
    20: 909038012,
    21: 909051003
}

LOOK_MAP = {
    0: 914000001,
    1: 914000002,
    2: 914000003,
    3: 914038001,
    4: 914039001,
    5: 914042001,
    6: 914044001,
    7: 914047001,
    8: 914047002,
    9: 914048001,
    10: 914050001,
    11: 914051001
}

# Badge values for s1 to s8 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 64,         # Your fourth badge
    "s5": 262144     # Your seventh badge
}


# Helper functions for ghost join
def dec_to_hex(decimal):
    """Convert decimal to hex string"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()
#------only admin can do some msgs-----#
def is_admin(uid):
    return str(uid) in ADMIN_UID
#--------timestamp to humantime --------#   
def xtimestamp(stamp):
      timestamp_value = int(stamp)
      datetime_object = datetime.fromtimestamp(timestamp_value)
      formatted_time = datetime_object.strftime("%b-%d-%Y %I:%M %p")
      return formatted_time

async def encrypt_packet(packet_hex, key, iv):
    """Encrypt packet using AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper for encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    
def friend_list_add(target_uid):
    try:
        url = f"https://danger-add-friend.vercel.app/adding_friend?uid=4210598764&password=D76B9581330C8899873F88B8CFCED603DD89B659F42F4E248975DC2C52612E61&friend_uid={target_uid}"
        res = requests.get(url)
        if res.status_code != 100:
            data = res.json()
            result = data.get('status', None)
            if result:
                return result
            else:
                return "Something Wrong With API"
        else:
            return f"Error Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"
        
def friend_list_remove(target_uid):
    try:
        url = f"https://danger-add-friend.vercel.app/remove_friend?uid=4210598764&password=D76B9581330C8899873F88B8CFCED603DD89B659F42F4E248975DC2C52612E61&friend_uid={target_uid}"
        res = requests.get(url)
        if res.status_code != 100:
            data = res.json()
            result = data.get('status', None)
            if result:
                return result
            else:
                return "Something Wrong With API"
        else:
            return f"Error Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"


def get_idroom_by_idplayer(packet_hex):
    """Extract room ID from packet - converted from your other TCP"""
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Error extracting room ID: {e}")
        return None

async def check_player_in_room(target_uid, key, iv):
    """Check if player is in a room by sending status request"""
    try:
        # Send status request packet
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        
        # You'll need to capture the response packet and parse it
        # For now, return True and we'll handle room detection in the main loop
        return True
    except Exception as e:
        print(f"Error checking player room status: {e}")
        return False
        
        
        


class MultiAccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.accounts_data = self.load_accounts()
    
    def load_accounts(self):
        """Load multiple accounts from JSON file"""
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)

                return accounts
        except FileNotFoundError:
            print(f"❌ Accounts file {self.accounts_file} not found!")
            return {}
        except Exception as e:
            print(f"❌ Error loading accounts: {e}")
            return {}
    
    
    
    async def get_account_token(self, uid, password):
        """Get access token for a specific account"""
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        open_id = data.get("open_id")
                        access_token = data.get("access_token")
                        return open_id, access_token
            return None, None
        except Exception as e:
            print(f"❌ Error getting token for {uid}: {e}")
            return None, None
    
    async def send_join_from_account(self, target_uid, account_uid, password, key, iv, region):
        """Send join request from a specific account"""
        try:
            # Get token for this account
            open_id, access_token = await self.get_account_token(account_uid, password)
            if not open_id or not access_token:
                return False
            
            # Create join packet using the account's credentials
            join_packet = await self.create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
            if join_packet:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error sending join from {account_uid}: {e}")
            return False
            
async def SEnd_InV_With_Cosmetics(Nu, Uid, K, V, region):
    """Simple version - just add field 5 with basic cosmetics"""
    region = "ind"
    fields = {
        1: 2, 
        2: {
            1: int(Uid), 
            2: region, 
            4: int(Nu),
            # Simply add field 5 with basic cosmetics
            5: {
                1: "BOT",                    # Name
                2: int(await get_random_avatar()),     # Avatar
                5: random.choice([1048576, 32768, 2048]),  # Random badge
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)   
            
async def join_custom_room(room_id, room_password, key, iv, region):
    """Join custom room with proper Free Fire packet structure"""
    fields = {
        1: 61,  # Room join packet type (verified for Free Fire)
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),  # Room ID
                2: int(time.time()),  # Timestamp
                3: "BOT",  # Player name
                5: 12,  # Unknown
                6: 9999999,  # Unknown
                7: 1,  # Unknown
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,  # Room type
            },
            3: str(room_password),  # Room password
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
    
async def leave_squad(key, iv, region):
    """Leave squad - converted from your old TCP leave_s()"""
    fields = {
        1: 7,
        2: {
            1: 12480598706  # Your exact value from old TCP
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def KickTarget(target_uid, key, iv):
    fields = {1: 35, 2: {1: int(target_uid)}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515' , key, iv)
    
async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    """Send join request with specific badge - converted from your old TCP"""
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] NIVA",
            7: 330,
            8: 1,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            16: 1,
            17: 1,
            18: 1,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: 902000013,
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value  # Dynamic badge value
            },
            32: badge_value,    # Dynamic badge value
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    
    packet = (await CrEaTe_ProTo(fields)).hex()
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk(packet, packet_type, key, iv)    
    
async def reset_bot_state(key, iv, region):
    """Reset bot to solo mode before spam - Critical step from your old TCP"""
    try:
        # Leave any current squad (using your exact leave_s function)
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        
        print("✅ Bot state reset - left squad")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting bot: {e}")
        return False    
    
async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    """Create a custom room"""
    fields = {
        1: 3,  # Create room packet type
        2: {
            1: room_name,
            2: room_password,
            3: max_players,  # 2, 4, 8, 16, etc.
            4: 1,  # Room mode
            5: 1,  # Map
            6: "en",  # Language
            7: {   # Player info
                1: "BotHost",
                2: int(await get_random_avatar()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)              
            
async def real_multi_account_join(target_uid, key, iv, region):
    """Send join requests using real account sessions"""
    try:
        # Load accounts
        accounts_data = load_accounts()
        if not accounts_data:
            return 0, 0
        
        success_count = 0
        total_accounts = len(accounts_data)
        
        for account_uid, password in accounts_data.items():
            try:
                print(f"🔄 Authenticating account: {account_uid}")
                
                # Get proper tokens for this account
                open_id, access_token = await GeNeRaTeAccEss(account_uid, password)
                if not open_id or not access_token:
                    print(f"❌ Failed to authenticate {account_uid}")
                    continue
                
                # Create a proper join request using the account's identity
                # We'll use the existing SEnd_InV function but with account context
                join_packet = await create_authenticated_join(target_uid, account_uid, key, iv, region)
                
                if join_packet:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                    success_count += 1
                    print(f"✅ Join sent from authenticated account: {account_uid}")
                
                # Important: Wait between requests
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error with account {account_uid}: {e}")
                continue
        
        return success_count, total_accounts
        
    except Exception as e:
        print(f"❌ Multi-account join error: {e}")
        return 0, 0



async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Reset bot state
        await reset_bot_state(key, iv, region)
        
        # Create and send join packets
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 10
        
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.01)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent {spam_count} Join Requests!\n🎯 Target: {target_uid}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        
async def handle_badge_commander(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    """Handle individual badge commands"""
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]❌ Usage: /{cmd} (uid)\nExample: /{cmd} 123456789\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid}...\n"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        # Reset bot state
        await reset_bot_state(key, iv, region)
        
        # Create and send join packets
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 1
        
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.5)
        
        success_msg = f"[B][C][00FF00]✅ Successfully Sent {spam_count} Join Requests!\n🎯 Target: {target_uid}\n🏷️ Badge: {badge_value}\n"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error in /{cmd}: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    """Create join request that appears to come from the specific account"""
    try:
        # Use the standard invite function but ensure it uses account context
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        print(f"❌ Error creating join packet: {e}")
        return None        
    
    async def create_account_join_packet(self, target_uid, account_uid, open_id, access_token, key, iv, region):
        """Create join request packet for specific account"""
        try:
            # This is where you use the account's actual UID instead of main bot UID
            fields = {
                1: 33,
                2: {
                    1: int(target_uid),  # Target UID
                    2: region.upper(),
                    3: 1,
                    4: 1,
                    5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                    6: f"BOT:[C][B][FF0000] ACCOUNT_{account_uid[-4:]}",  # Show account UID
                    7: 330,
                    8: 1000,
                    10: region.upper(),
                    11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                               97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                    12: 1,
                    13: int(account_uid),  # Use the ACCOUNT'S UID here, not target UID!
                    14: {
                        1: 2203434355,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    },
                    16: 1,
                    17: 1,
                    18: 312,
                    19: 46,
                    23: bytes([16, 1, 24, 1]),
                    24: int(await get_random_avatar()),
                    26: "",
                    28: "",
                    31: {
                        1: 1,
                        2: 32768  # V-Badge
                    },
                    32: 32768,
                    34: {
                        1: int(account_uid),  # Use the ACCOUNT'S UID here too!
                        2: 8,
                        3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
                    }
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                }
            }
            
            packet = (await CrEaTe_ProTo(fields)).hex()
            
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
                
            return await GeneRaTePk(packet, packet_type, key, iv)
            
        except Exception as e:
            print(f"❌ Error creating join packet for {account_uid}: {e}")
            return None

# Global instance
multi_account_manager = MultiAccountManager()
    
    
    
async def auto_rings_emote_dual(sender_uid, key, iv, region):
    """Send The Rings emote to both sender and bot for dual emote effect"""
    try:
        # The Rings emote ID
        rings_emote_id = 90905000
        
        # Get bot's UID
        bot_uid = 13699776666
        
        # Send emote to SENDER (person who invited)
        emote_to_sender = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        
        # Small delay between emotes
        await asyncio.sleep(0.5)
        
        # Send emote to BOT (bot performs emote on itself)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
        
        print(f"🤖 Bot performed dual Rings emote with sender {sender_uid} and bot {bot_uid}!")
        
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")    
        
        
async def Room_Spam(Uid, Rm, Nm, K, V):
   
    same_value = random.choice([32768])  #you can add any badge value 
    
    fields = {
        1: 78,
        2: {
            1: int(Rm),  
            2: "iG:[C][B][FF0000] KALLU CODEX",  
            3: {
                2: 1,
                3: 1
            },
            4: 330,      
            5: 6000,     
            6: 201,      
            10: 902000013,  
            11: int(Uid), # Target UID
            12: 1,       
            15: {
                1: 1,
                2: same_value  
            },
            16: same_value,    
            18: {
                1: 11481904755,  
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            
            31: {
                1: 1,
                2: same_value  
            },
            32: same_value,    
            34: {
                1: int(Uid),   
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)
    
async def evo_cycle_spam(uids, key, iv, region):
    """Cycle through all evolution emotes one by one with 5-second delay"""
    global evo_cycle_running
    
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
                
            print(f"Sending evolution emote {emote_number} (ID: {emote_id})")
            
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                    print(f"Sent emote {emote_number} to UID: {uid}")
                except Exception as e:
                    print(f"Error sending evo emote {emote_number} to {uid}: {e}")
            
            # Wait 5 seconds before moving to next emote (as requested)
            if evo_cycle_running:
                print(f"Waiting 5 seconds before next emote...")
                for i in range(6):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        
        # Small delay before restarting the cycle
        if evo_cycle_running:
            print("Completed one full cycle of all evolution emotes. Restarting...")
            await asyncio.sleep(2)
    
    print("Evolution emote cycle stopped")
    
async def reject_spam_loop(target_uid, key, iv):
    """Send reject spam packets to target in background"""
    global reject_spam_running
    
    count = 0
    
    while reject_spam_running:
        try:
            # Send both packets
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            
            # Send to Online connection
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            
            count += 1
            print(f"Sent reject spam #{count} to {target_uid}")
            
            # 0.5 second delay between spam cycles
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    
    return count    
    
async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    """Handle completion of reject spam and send final message"""
    try:
        spam_count = await spam_task
        
        # Send completion message
        if spam_count >= 150:
            completion_msg = f"[B][C][00FF00]✅ Reject Spam Completed Successfully for ID {target_uid}\n✅ Total packets sent: {spam_count * 2}\n"
        else:
            completion_msg = f"[B][C][FFFF00]⚠️ Reject Spam Partially Completed for ID {target_uid}\n⚠️ Total packets sent: {spam_count * 2}\n"
        
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
        
    except asyncio.CancelledError:
        print("Reject spam was cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ ERROR in reject spam: {str(e)}\n"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)    
    
async def banecipher(client_id, key, iv):
    """Create reject spam packet 1 - Converted to new async format"""
    banner_text = f"""[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._
[0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._ [0F7209]INSTAGRAM:-    [FF0000]@ft_rosie._"""        
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    """Create reject spam packet 2 - Converted to new async format"""
    gay_text = f"""."""        
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    
    # Use CrEaTe_ProTo from xC4.py (async)
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    
    # Build final packet based on header length
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet

    return bytes.fromhex(final_packet)
    

async def lag_team_loop(team_code, key, iv, region):
    """Rapid join/leave loop to create lag"""
    global lag_running
    count = 0
    
    while lag_running:
        try:
            # Join the team
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
            # Very short delay before leaving
            await asyncio.sleep(0.01)  # 10 milliseconds
            
            # Leave the team
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            
            count += 1
            print(f"Lag cycle #{count} completed for team: {team_code}")
            
            # Short delay before next cycle
            await asyncio.sleep(0.01)  # 10 milliseconds between cycles
            
        except Exception as e:
            print(f"Error in lag loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)
 
################################

async def fun_group_change(uid, key, iv, region):
    """rotate 6 and 5 member lobby to make fun"""
    global fun_group_running
    count = 0
    
    while fun_group_running:
        try:
            # Join the team
            C = await cHSq(5, uid, key, iv, region)
            await asyncio.sleep(0.2)  # Reduced delay
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.2)
            D = await cHSq(6, uid, key, iv, region)
            await asyncio.sleep(0.2)  # Reduced delay
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', D)
            
            count += 1
            print(f"Fun Cycle #{count} Completed")
            
            # Short delay before next cycle
            await asyncio.sleep(0.2)  # 10 milliseconds between cycles
            
        except Exception as e:
            print(f"Error in fun loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)
            
################################

async def fun_room_spam(Uid, Rm, Nm, K, V):
    """join room spam to make fun"""
    global fun_rspam_running
    count = 0
    
    while fun_rspam_running:
        try:
            NIVA = await Room_Spam(Uid, Rm, Nm, K, V)
            await asyncio.sleep(0.1)  # Reduced delay
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', NIVA)
            
            count += 1
            print(f"Fun spam #{count} Completed")
            
            # Short delay before next cycle
            await asyncio.sleep(1)  # 1 seconds between cycles
            
        except Exception as e:
            print(f"Error in fun loop: {e}")
            # Continue the loop even if there's an error
            await asyncio.sleep(0.1)
 
################################
#Clan-info-by-clan-id
def get_guild_info(uid):
    try:
            url = f"https://mafuuuu-info-api.vercel.app/mafu-info?uid={uid}"
            response = requests.get(url)
            error = f"""[11EAFD][b][c]°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
Failed to get info, please try again later!!

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°"""
            data = response.json()
            name= data.get('basicInfo', {}).get('nickname', None)
            account_uid= data.get('basicInfo', {}).get('accountId', None)
            account_create= data.get('basicInfo', {}).get('createAt', None)
            last_login = data.get('basicInfo', {}).get('lastLoginAt', None)
            level= data.get('basicInfo', {}).get('level', None)
            exp= data.get('basicInfo', {}).get('exp', None)
            like= data.get('basicInfo', {}).get('liked', None)
            region= data.get('basicInfo', {}).get('region', None)
            prime_badge= data.get('basicInfo', {}).get('primeLevel', {}).get('primeLevel', None)
            guild_name= data.get('clanBasicInfo', {}).get('clanName', None)
            guild_uid= data.get('clanBasicInfo', {}).get('clanId', None)
            guild_cap= data.get('clanBasicInfo', {}).get('capacity', None)
            guild_member= data.get('clanBasicInfo', {}).get('memberNum', None)
            guild_leader_uid= data.get('clanBasicInfo', {}).get('captainId', None)
            guild_lvl= data.get('clanBasicInfo', {}).get('clanLevel', None)
            pet= data.get('petInfo', {}).get('name', None)
            guild_leader= data.get('captainBasicInfo', {}).get('nickname', None)
            guild_leader_online= data.get('captainBasicInfo', {}).get('lastLoginAt', None)
            bio= data.get('socialInfo', {}).get('signature', None)
            honor= data.get('creditScoreInfo', {}).get('creditScore', None)
            create_format = f"{xtimestamp(account_create)}"
            lastlogin_format = f"{xtimestamp(last_login)}"
            guild_leader_online_format = f"{xtimestamp(guild_leader_online)}"
            no_guild = f"""[66FF00]{name} Not In Guild"""
            msg = f"""[C][B][FF99FF]━━━━[FFFFFF]FREE F[FFD700]I[FFFFFF]RE[FF99FF]━━━━\n
[6600FF]Player's Guild Info :-\n
[FFFFFF]Name: [66FF00]{guild_name}
[FFFFFF]Id: [66FF00]{xMsGFixinG(guild_uid)}
[FFFFFF]Level: [66FF00]{guild_lvl}
[FFFFFF]Capacity: [66FF00]{guild_cap}
[FFFFFF]Members: [66FF00]{guild_member}
[FFFFFF]Leader Name: [66FF00]{guild_leader}
[FFFFFF]Leader Uid: [66FF00]{xMsGFixinG(guild_leader_uid)}
[FFFFFF]Leader Last Login On:
[66FF00]{xMsGFixinG(guild_leader_online_format)}

[FF99FF]━━━━━━━━━━━━"""
            if response.status_code == 200:
                
                if "captainBasicInfo" in data:
                     return msg
                else:
                     return no_guild
            else:
                return error
    except:
       pass
#GET INFO BY PLAYER ID
def get_player_info(uid):
    try:
       url = f"https://mafuuuu-info-api.vercel.app/mafu-info?uid={uid}"
       response = requests.get(url)
       if response.status_code == 200:
            data = response.json()
            name= data.get('basicInfo', {}).get('nickname', None)
            account_uid= data.get('basicInfo', {}).get('accountId', None)
            account_create= data.get('basicInfo', {}).get('createAt', None)
            last_login = data.get('basicInfo', {}).get('lastLoginAt', None)
            level= data.get('basicInfo', {}).get('level', None)
            exp= data.get('basicInfo', {}).get('exp', None)
            like= data.get('basicInfo', {}).get('liked', None)
            region= data.get('basicInfo', {}).get('region', None)
            prime_badge= data.get('basicInfo', {}).get('primeLevel', {}).get('primeLevel', None)
            guild_name= data.get('guildInfo', {}).get('clanName', None)
            guild_uid= data.get('guildInfo', {}).get('clanId', None)
            guild_cap= data.get('guildInfo', {}).get('capacity', None)
            guild_member= data.get('guildInfo', {}).get('memberNum', None)
            guild_leader_uid= data.get('guildInfo', {}).get('captainId', None)
            guild_lvl= data.get('guildInfo', {}).get('clanLevel', None)
            pet= data.get('petInfo', {}).get('name', None)
            guild_leader= data.get('guildOwnerInfo', {}).get('nickname', None)
            bio= data.get('socialInfo', {}).get('signature', None)
            honor= data.get('creditScoreInfo', {}).get('creditScore', None)
            create_format = f"{xtimestamp(account_create)}"
            lastlogin_format = f"{xtimestamp(last_login)}"
            return f"""[C][B][FF99FF]━━━━[FFFFFF]FREE F[FFD700]I[FFFFFF]RE[FF99FF]━━━━\n
[6600FF]Player's Info :-\n
[FFFFFF]Name: [66FF00]{name}
[FFFFFF]Level: [66FF00]{level} [FFFFFF]([66FF00]{xMsGFixinG(exp)}[FFFFFF])
[FFFFFF]Like: [66FF00]{xMsGFixinG(like)}
[FFFFFF]Region: [66FF00]{region}
[FFFFFF]Honor Score: [66FF00]{honor}
[FFFFFF]Pet Name: [66FF00]{pet}
[FFFFFF]Last Login On:
[66FF00]{xMsGFixinG(lastlogin_format)}
[FFFFFF]Account Created On:
[66FF00]{xMsGFixinG(create_format)}
[FFFFFF]Bio:
[/b][/c]{bio}

[FF99FF]━━━━━━━━━━━━"""
    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Info API Connection Failed!"
    except Exception as e:
        return f"[B][C][FF0000]❌ Unexpected Error: {str(e)}"
            

 
#GET PLAYER BIO 
def get_player_bio(uid):
    try:
        url = f"https://mafuuuu-info-api.vercel.app/mafu-info?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Bio is inside socialInfo -> signature
            bio = data.get('socialInfo', {}).get('signature', None)
            if bio:
                return bio
            else:
                return "No bio available"
        else:
            return f"Failed to fetch bio. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"
        
def get_ghost_join(teamcode):
    try:
        url = f"https://ghost-v97q.onrender.com/niva?teamcode={teamcode}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # Bio is inside socialInfo -> signature
            bio = data.get('socialInfo', {}).get('signature', None)
            if bio:
                return bio
            else:
                return "Ghost Joining"
        else:
            return f"Failed to Join Ghost. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

def get_player_name(uid):
    try:
        url = f"https://mafuuuu-info-api.vercel.app/mafu-info?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            # name is inside basicInfo -> nickname
            name = data.get('basicInfo', {}).get('nickname', None)
            if name:
                return name
            else:
                return "Error"
        else:
            return f"Failed to fetch name. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

#CHAT WITH AI
def talk_with_ai(question):
  try:
    url = f"https://princeaiapi.vercel.app/prince/api/v1/ask?key=prince&ask=hello{question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        ai_answer = data.get('message', {}).get('content', None)
        if ai_answer:
                return ai_answer
        else:
                return "Error to talk with Ai"
    else:
        return f"Failed to connect with Ai error:{res.status_code}"
  except Exception as e:
    return f"Error occurred: {e}"
#SPAM REQUESTS
def spam_requests(player_id):
    # This URL now correctly points to the Flask app you provided
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20) # Added a timeout
        if res.status_code == 200:
            data = res.json()
            # Return a more descriptive message based on the API's JSON response
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            # Return the error status from the API
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        # Handle cases where the API isn't running or is unreachable
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."
####################################

# ** NEW INFO FUNCTION using the new API **
def newinfo(uid):
    # Base URL without parameters
    url = "https://like2.vercel.app/player-info"
    # Parameters dictionary - this is the robust way to do it
    params = {
        'uid': uid,
        'server': server2,  # Hardcoded to bd as requested
        'key': key2
    }
    try:
        # Pass the parameters to requests.get()
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the expected data structure is in the response
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                # The API returned 200, but the data is not what we expect (e.g., error message in JSON)
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            # The API returned an error status code (e.g., 404, 500)
            try:
                # Try to get a specific error message from the API's response
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                # If the error response is not JSON
                return {"status": "error", "message": f"API returned status {response.status_code}"}

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., timeout, no connection)
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError: 
        # Handle cases where the response is not valid JSON
        return {"status": "error", "message": "Invalid JSON response from API."}
        
    async def run_spam(chat_type, message, count, uid, chat_id, key, iv):
        try:
            for i in range(count):
                await safe_send_message(chat_type, message, uid, chat_id, key, iv)
                await asyncio.sleep(0.12)
        except Exception as e:
            print("Spam Error:", e)
            
async def bundle_packet_async(bundle_id, key, iv, region="ind"):
    """Create bundle packet"""
    bundle = LOOK_MAP.get(int(bundle_id))
    fields = {
        1: 88,
        2: {
            1: {
                1: bundle,
                2: 1
            },
            2: 2
        }
    }
    
    # Use your CrEaTe_ProTo function
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Use your encrypt_packet function
    encrypted = await encrypt_packet(packet_hex, key, iv)
    
    # Use your DecodE_HeX function
    header_length = len(encrypted) // 2
    header_length_hex = await DecodE_HeX(header_length)
    
    # Build final packet based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    
    # Determine header based on length
    if len(header_length_hex) == 2:
        final_header = f"{packet_type}000000"
    elif len(header_length_hex) == 3:
        final_header = f"{packet_type}00000"
    elif len(header_length_hex) == 4:
        final_header = f"{packet_type}0000"
    elif len(header_length_hex) == 5:
        final_header = f"{packet_type}000"
    else:
        final_header = f"{packet_type}000000"
    
    final_packet_hex = final_header + header_length_hex + encrypted
    return bytes.fromhex(final_packet_hex)
        
def send_title_msg(self, chat_id, key, iv):
        """Build title packet using dictionary structure like GenResponsMsg"""
    
        fields = {
            1: 1,  # type
            2: {   # data
                1: int(self),  # uid
                2: str(chat_id),   # chat_id  
                3: f"{{\"TitleID\":904990071,\"type\":\"Title\"}}",  # title
                4: int(datetime.now().timestamp()),  # timestamp
                5: 0,   # chat_type
                6: "en", # language
                9: {    # field9 - player details
                    1: "[C][B][FF0000] KRN ON TOP",  # Nickname
                    2: 902000013,          # avatar_id
                    3: 330,                          # rank
                    4: 102000015,                    # badge
                    5: "TEMP GUILD",                 # Clan_Name
                    6: 1,                            # field10
                    7: 1,                            # global_rank_pos
                    8: {                             # badge_info
                        1: 2                         # value
                    },
                    9: {                             # prime_info
                        1: 1158053040,               # prime_uid
                        2: 8,                        # prime_level
                        3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"  # prime_hex
                    }
                },
                13: {   # field13 - url options
                    1: 2,   # url_type
                    2: 1    # curl_platform
                },
                99: b""  # empty_field
            }
        }

        # **EXACTLY like GenResponsMsg:**
        packet = CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
    
    # Use EnC_PacKeT from xC4.py (async)
        encrypted_packet = EnC_PacKeT(packet_hex, key, iv)
    
    # Calculate header length
        header_length = len(encrypted_packet) // 2
        header_length_final = DecodE_HeX(header_length)
    
        # **KEY: Use 0515 for title packets instead of 1215**
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
    
        return bytes.fromhex(final_packet)
        
async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)
    
async def RejectMSGtaxt(squad_owner,uid, key, iv):
    random_banner = f"""[c][FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._
[FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._ [FF0099]INSTAGRAM:-    [66FF00]@ft_rosie._"""
    fields = {
    1: 5,
    2: {
        1: int(squad_owner),
        2: 1,
        3: int(uid),
        4: random_banner
    }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , key, iv)

	
#ADDING-100-LIKES-IN-24H
def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
             timeout=15
             )
      
      
        if likes_api_response.status_code != 200:
            return f"""
[C][B][FF0000]━━━━━
[FFFFFF]Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
━━━━━
"""

        api_json_response = likes_api_response.json()

        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # ✅ Success
            return f"""
[C][B][11EAFD]‎━━━━━━━━━━━━
[FFFFFF]Likes Status:

[00FF00]Likes Sent Successfully!

[FFFFFF]Player Name : [00FF00]{player_name}  
[FFFFFF]Likes Added : [00FF00]{likes_added}  
[FFFFFF]Likes Before : [00FF00]{likes_before}  
[FFFFFF]Likes After : [00FF00]{likes_after}  
[C][B][11EAFD]‎━━━━━━━━━━━━
[C][B][FFB300]Subscribe: [FFFFFF]SPIDEERIO YT [00FF00]!!
"""
        elif status == 2 or likes_before == likes_after:
            # 🚫 Already claimed / Maxed
            return f"""
[C][B][FF0000]━━━━━━━━━━━━

[FFFFFF]No Likes Sent!

[FF0000]You have already taken likes with this UID.
Try again after 24 hours.

[FFFFFF]Player Name : [FF0000]{player_name}  
[FFFFFF]Likes Before : [FF0000]{likes_before}  
[FFFFFF]Likes After : [FF0000]{likes_after}  
[C][B][FF0000]━━━━━━━━━━━━
"""
        else:
            # ❓ Unexpected case
            return f"""
[C][B][FF0000]━━━━━━━━━━━━
[FFFFFF]Unexpected Response!
Something went wrong.

Please try again or contact support.
━━━━━━━━━━━━
"""

    except requests.exceptions.RequestException:
        return """
[C][B][FF0000]━━━━━
[FFFFFF]Like API Connection Failed!
Is the API server (app.py) running?
━━━━━
"""
    except Exception as e:
        return f"""
[C][B][FF0000]━━━━━
[FFFFFF]An unexpected error occurred:
[FF0000]{str(e)}
━━━━━
"""
#USERNAME TO INSTA INFO 
def send_insta_info(username):
    try:
        response = requests.get(f"https://kallu-insta-info-api.vercel.app/api/insta/{username}", timeout=15)
        if response.status_code != 200:
            return f"[B][C][FF0000]❌ Instagram API Error! Status Code: {response.status_code}"

        user = response.json()
        full_name = user.get("full_name", "Unknown")
        followers = user.get("edge_followed_by", {}).get("count") or user.get("followers_count", 0)
        following = user.get("edge_follow", {}).get("count") or user.get("following_count", 0)
        posts = user.get("media_count") or user.get("edge_owner_to_timeline_media", {}).get("count", 0)
        profile_pic = user.get("profile_pic_url_hd") or user.get("profile_pic_url")
        private_status = user.get("is_private")
        verified_status = user.get("is_verified")
        bio = user.get("biography")

        return f"""[B][C][FB0364]╭[D21A92]─[BC26AB]╮[FFFF00]╔═══════╗
[C][B][FF7244]│[FE4250]◯[C81F9C]֯│[FFFF00]║[FFFFFF]INSTAGRAM_INFO[FFFF00]║
[C][B][FDC92B]╰[FF7640]─[F5066B]╯[FFFF00]╚═══════╝
[C][B][FFFF00]━━━━━━━━━━━━
[C][B][FFFFFF]Name: [66FF00]{full_name}
[C][B][FFFFFF]Username: [66FF00]{username}
[C][B][FFFFFF]Followers: [66FF00]{followers}
[C][B][FFFFFF]Following: [66FF00]{following}
[C][B][FFFFFF]Posts: [66FF00]{posts}
[C][B][FFFFFF]Private: [66FF00]{private_status}
[C][B][FFFFFF]Verified: [66FF00]{verified_status}
[C][B][FFFF00]━━━━━━━━━━━━"""
    except requests.exceptions.RequestException:
        return "[B][C][FF0000]❌ Instagram API Connection Failed!"
    except Exception as e:
        return f"[B][C][FF0000]❌ Unexpected Error: {str(e)}"

####################################
#CHECK ACCOUNT IS BANNED

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB53"}

# ---- Random Colores ----
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

    
# ---- Random Avatar ----
async def get_random_avatar():
    await asyncio.sleep(0)  # makes it async but instant
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004',
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    return random.choice(avatar_list)
    
#print(get_random_avatar())

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    """Join team, authenticate chat, perform emote, and leave automatically"""
    try:
        # Step 1: Join the team
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"🤖 Joined team: {team_code}")
        
        # Wait for team data and chat authentication
        await asyncio.sleep(0.2)  # Increased to ensure proper connection
        
        # Step 2: The bot needs to be detected in the team and authenticate chat
        # This happens automatically in TcPOnLine, but we need to wait for it
        
        # Step 3: Perform emote to target UID
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"🎭 Performed emote {emote_id} to UID {target_uid}")
        
        # Wait for emote to register
        await asyncio.sleep(0)
        
        # Step 4: Leave the team
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"🚪 Left team: {team_code}")
        
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
        
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"
        
        
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "2.124.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    """Safely send message with retry mechanism"""
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)  # Wait before retry
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    """Fast emote spam function that sends emotes rapidly"""
    global fast_spam_running
    count = 0
    max_count = 50  # Spam 50 times
    
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.05)  # 0.1 seconds interval between spam cycles

# NEW FUNCTION: Custom emote spam with specified times
async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    """Custom emote spam function that sends emotes specified number of times"""
    global custom_spam_running
    count = 0
    
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.05)  # 0.1 seconds interval between emotes
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break

# NEW FUNCTION: Faster spam request loop - Sends exactly 30 requests quickly
async def spam_request_loop(target_uid, key, iv, region):
    """Spam request function - using your same structure"""
    global spam_request_running
    
    count = 0
    max_requests = 30
    
    
    while spam_request_running and count < max_requests:
        try:
            # Create squad (same as before)
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.45)
            
            # Change squad size (same as before)
            C = await cHSq(4, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.45)
            
            # Send invite
            V = await SEnd_InV(4, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            await asyncio.sleep(0.1)
            
            # Leave squad (same as before)
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            
            count += 1
            print(f"✅ Sent cosmetic invite #{count} to {target_uid}")
            
            # Short delay
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"Error in spam: {e}")
            await asyncio.sleep(0.5)
    
    return count
            


# NEW FUNCTION: Evolution emote spam with mapping
async def evo_emote_spam(uids, number, key, iv, region):
    """Send evolution emotes based on number mapping"""
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")
        
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"

# NEW FUNCTION: Fast evolution emote spam
async def evo_fast_emote_spam(uids, number, key, iv, region):
    """Fast evolution emote spam function"""
    global evo_fast_spam_running
    count = 0
    max_count = 50  # Spam 25 times
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.05)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed fast evolution emote spam {count} times"

# NEW FUNCTION: Custom evolution emote spam with specified times
async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    """Custom evolution emote spam with specified repeat times"""
    global evo_custom_spam_running
    count = 0
    
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")
        
        count += 1
        await asyncio.sleep(0.05)  # CHANGED: 0.5 seconds to 0.1 seconds
    
    return True, f"Completed custom evolution emote spam {count} times"

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.1):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, insquad, joining_team, evo_custom_spam_running, evo_custom_spam_task, fun_group_running, fun_group_task, fun_rspam_running, fun_rspam_task, lag_running, lag_task
    
    if insquad is not None:
        insquad = None
    if joining_team is True:
        joining_team = False
    
    online_writer = None
    whisper_writer = None
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0514'):
                    try:
                        # Try to extract emote info from encrypted packet
                        decrypted = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(decrypted)
                        print (f"{packet_json}")
                        emote_id = str(packet_json['2']['data']['5']['data']['3']['data'])
                        print (f"{emote_id}")
                        bot_uid = "13513476553"
                        bot_self_emote = await Emote_k(bot_uid, emote_id, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_self_emote)
                    except Exception as e:
                        print(f"❌ Emote hijack error: {e}")
                        pass
                        
                        


                # =================== AUTO ACCEPT HANDLING ===================
                
                # Case 1: Squad is cancelled or left
                if data2.hex().startswith('0500') and insquad is not None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet)
                        
                        if packet_json.get('1') in [6, 7]: 
                             insquad = None
                             joining_team = False
                             print("Squad cancelled or exited (code 6/7).")
                             continue
                             
                    except Exception as e:
                        print(f"Error in auto-accept case 1: {e}")
                        pass
                
                # Case 2: Receiving an invitation while not in a squad (Auto-Join/Accept)
                if data2.hex().startswith("0500"):
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet)
                        
                        uid = packet_json['5']['data']['1']['data']
                        invite_uid = packet_json['5']['data']['2']['data']['1']['data']
                        squad_owner = packet_json['5']['data']['1']['data']
                        code = packet_json['5']['data']['8']['data']
                        emote_id = 909050009
                        bot_uid = 14009897329
                            
                        
                        inv_packet = await RejectMSGtaxt(squad_owner, uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', inv_packet)
                        
                            
                        print(f"Received squad invite from {squad_owner}, accepting...")                  
                        Join = await ArohiAccepted(squad_owner, code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                            
                        await asyncio.sleep(2)

                        insquad = True
                            
                    except Exception as e:
                        print(f"Auto-accept error: {e}")
                        joining_team = False
                        continue
               # case 5
                if insquad == True:
                    try:
                        # Assuming DeCode_PackEt, json.loads, GeTSQDaTa, AutH_Chat, SEndPacKeT are available
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet)
                        
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        
                        print(f"Received squad data for joining team, attempting chat auth for {OwNer_UiD}...")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        
                        
                        message = """122809569"""
                        # In your auto-join (Old Handler) code, find this line:

                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                        joining_team = False
                        insquad = None
                            
                    except Exception as e:
                        print(f"Error in joining_team chat auth: {e}")
                        # Removed the redundant inner try/except block.
                        pass
                
                # Case 3: Joining Team/Chat handling (long packet)
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000 and joining_team:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet)
                        
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        
                        print(f"Received squad data for joining team, attempting chat auth for {OwNer_UiD}...")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        
                        joining_team = False
                            
                    except Exception as e:
                        print(f"Error in joining_team chat auth: {e}")
                        pass
                
         
                
                # Case 4: General Chat Auth (long packet, not actively joining)
                if data2.hex().startswith('120') and len(data2.hex()) > 100:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet_json = json.loads(packet)
                        
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)

                        print(f"Received long packet, attempting general chat auth for {OwNer_UiD}...")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                    except Exception as e:
                        print(f"Error in general chat auth: {e}")
                        pass
        
                if data2.hex().startswith('0f00') and len(data2.hex()) > 100:
                    print(f"📡 Received status response packet")
    
                    try:
                        if '08' in data2.hex():
                            proto_part = f'08{data2.hex().split("08", 1)[1]}'
                        else:
                            print("⚠️ Status packet structure missing '08' marker.")
                            continue
        
                        parsed_data = get_available_room(proto_part)
                        if parsed_data:
                            parsed_json = json.loads(parsed_data)
            
                            if "2" in parsed_json and parsed_json["2"]["data"] == 15:
                                player_id = parsed_json["5"]["data"]["1"]["data"]["1"]["data"]
                                player_status = get_player_status(proto_part) 
                                print(f"✅ Parsed status for {player_id}: {player_status}")
                
                                cache_entry = {
                                    'status': player_status, 
                                    'packet': proto_part,
                                    'timestamp': time.time(),
                                    'full_packet': data2.hex(),
                                    'parsed_json': parsed_json
                                }
                
                                # --- SPECIAL CONDITION CHECK ---
                                try:
                                    StatusData = parsed_json
                                    if ("5" in StatusData and "data" in StatusData["5"] and 
                                        "1" in StatusData["5"]["data"] and "data" in StatusData["5"]["data"]["1"] and 
                                        "3" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["3"] and 
                                        StatusData["5"]["data"]["1"]["data"]["3"]["data"] == 1 and 
                                        "11" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["11"] and 
                                        StatusData["5"]["data"]["1"]["data"]["11"]["data"] == 1):
                
                                        print(f"🎯 SPECIAL CONDITION MET: Player {player_id} is in SOLO mode with special flag 11=1")
                                        cache_entry['special_state'] = 'SOLO_WITH_FLAG_1'
                
                                except Exception as cond_error:
                                    print(f"⚠️ Error checking special condition: {cond_error}")
                                
                                # Extract room ID if in room
                                if "IN ROOM" in player_status:
                                    try:
                                        room_id = get_idroom_by_idplayer(proto_part)
                                        if room_id:
                                            cache_entry['room_id'] = room_id
                                            print(f"🏠 Room ID extracted: {room_id}")
                                    except Exception as room_error:
                                        print(f"Failed to extract room ID: {room_error}")
                
                                # Extract leader if in squad
                                elif "INSQUAD" in player_status:
                                    try:
                                        leader_id = get_leader(proto_part)
                                        if leader_id:
                                            cache_entry['leader_id'] = leader_id
                                            print(f"👑 Leader ID: {leader_id}")
                                    except Exception as leader_error:
                                        print(f"Failed to extract leader: {leader_error}")
                
                                # Save to cache
                                # Assuming save_to_cache function exists
                                # save_to_cache(player_id, cache_entry)
                                print(f"✅ Status cache updated: {player_id} = {player_status}")
                
                    except Exception as e:
                        print(f"❌ Error parsing status: {e}")
                        import traceback
                        traceback.print_exc()
                

            # --- CLEANUP AFTER INNER LOOP (Connection closed) ---
            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
                
            insquad = None
            joining_team = False
            
            print(f"Connection Closed Securely")

        except ConnectionRefusedError:
            print(f"Connection refused to {ip}:{port}. Retrying...")
            await asyncio.sleep(reconnect_delay)
        except asyncio.TimeoutError:
            print(f"Connection timeout to {ip}:{port}. Retrying...")
            await asyncio.sleep(reconnect_delay)
        except Exception as e:
            print(f"Unexpected error in TcPOnLine: {e}")
            await asyncio.sleep(reconnect_delay)
        
                    

                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task, fun_group_running, fun_rspam_running, fun_rspam_task, fun_group_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        
                        # Debug print to see what we're receiving
                        print(f"Received message: {inPuTMsG} from UID: {uid} in chat type: {XX}")
                        
                    except:
                        response = None


                    if response:
                        # ALL COMMANDS NOW WORK IN ALL CHAT TYPES (SQUAD, GUILD, PRIVATE)
                        if inPuTMsG.startswith('/ee '):
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) >= 4:  # Minimum: /ee team_code uid1 uid2 emote_id
                                    team_code = parts[1]  # First parameter is team code
                                    uids = []
                                    emote_id = None
                                    
                                    # Middle parameters are UIDs, last parameter is emote_id
                                    for i, part in enumerate(parts[2:], 2):  # Start from index 2 (after team code)
                                        if i < len(parts) - 1:  # All except last parameter are UIDs
                                            if part.isdigit():
                                                uids.append(int(part))
                                        else:  # Last parameter is emote ID
                                            if part.isdigit():
                                                emote_id = int(part)
                                    
                                    if len(uids) >= 1 and emote_id:
                                        # Send processing message
                                        processing_msg = f"[FFD700][B]━━━━━━━\n[FFFFFF]Joining: {team_code}\n[FFFFFF]UIDs: {len(uids)}\n[FFFFFF]🎭 Emote: {emote_id}\n[FFD700]━━━━━━━"
                                        P = await safe_send_message(response.Data.chat_type, processing_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        
                                        # Step 1: Join the team using team code
                                        try:
                                            join_msg = f"[FF6347][B]🎯 Joining Team: {team_code}"
                                            P_join = await safe_send_message(response.Data.chat_type, join_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_join)
                                            
                                            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            await asyncio.sleep(0.2)  # Wait for join to complete
                                        except:
                                            pass
                                        
                                        # Step 2: Send emotes to all UIDs
                                        success_count = 0
                                        for target_uid in uids:
                                            try:
                                                H = await Emote_k(target_uid, emote_id, key, iv, region)
                                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                                success_count += 1
                                                await asyncio.sleep(0)  # Delay between emotes
                                            except:
                                                pass
                                        
                                        # Step 3: Immediately leave the team
                                        try:
                                            leave_msg = f"[FF0000][B]🚪 Leaving Team: {team_code}"
                                            P_leave = await safe_send_message(response.Data.chat_type, leave_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_leave)
                                            
                                            leave_packet = await ExiT(None, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                                        except:
                                            pass
                                        
                                        # Confirmation
                                        confirm_msg = f"[00FF00][B]━━━━━━━\n[FFFFFF]✅ Team Emote Complete!\n[FFFFFF]Success: {success_count}/{len(uids)}\n[FFFFFF]Team: {team_code}\n[FFFFFF]🔄 Auto-Leave: ✅\n[FFD700]━━━━━━━"
                                        P_confirm = await safe_send_message(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                                    else:
                                        error_msg = f"[FF0000]Usage: /ee [TEAM_CODE] [UID1] [UID2] [UID3] [EMOTE]\nExample: /ee FAST123 1234 5678 9012 1\n[B22222]Will auto-join team and leave after emotes"
                                        P = await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /ee [TEAM_CODE] [UID1] [UID2] [UID3] [EMOTE]\nExample: /ee FAST123 1234 5678 9012 1\n[B22222]Will auto-join team and leave after emotes"
                                    P = await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                error_msg = f"[FF0000]/ee command error"
                                P = await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            continue
                            
                        if inPuTMsG.strip().startswith('/add '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                if is_admin(uid):
                                  loop = asyncio.get_event_loop()
                                  with ThreadPoolExecutor() as executor:
                                    add_result = await loop.run_in_executor(executor, friend_list_add, target_uid)
                                  await safe_send_message(response.Data.chat_type, f"{add_result}", uid, chat_id, key, iv)
                                else:
                                  Others = f"Admin's Only Can Add Friendlist"
                                  await safe_send_message(response.Data.chat_type, Others, uid, chat_id, key, iv)
                                
                        if inPuTMsG.strip().startswith('/remove '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                if is_admin(uid):
                                  loop = asyncio.get_event_loop()
                                  with ThreadPoolExecutor() as executor:
                                    remove_result = await loop.run_in_executor(executor, friend_list_remove, target_uid)
                                  await safe_send_message(response.Data.chat_type, f"{remove_result}", uid, chat_id, key, iv)
                                else:
                                  Others = f"Admin's Only Can Remove Friendlist"
                                  await safe_send_message(response.Data.chat_type, Others, uid, chat_id, key, iv)
                                
                                
                        # AI Command - /ai
                        if inPuTMsG.strip().startswith('ami '):
                            print('Processing AI command in any chat type')
                            
                            question = inPuTMsG[4:].strip()
                            if question:
                                
                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ai_response = await loop.run_in_executor(executor, talk_with_ai, question)
                                
                                # Format the AI response
                                ai_message = f"""\n[c][66ff00]{ai_response}\n"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌[ffffff] ERROR! Please provide a question after ami\nExample: ami What is Free Fire?\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Likes Command - /likes
                        if inPuTMsG.strip().startswith('/likes '):
                            print('Processing likes command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /likes (uid)\nExample: /likes 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nSending 100 likes to {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    likes_result = await loop.run_in_executor(executor, send_likes, target_uid)
                                
                                await safe_send_message(response.Data.chat_type, likes_result, uid, chat_id, key, iv)
                                
                                #TEAM SPAM MESSAGE COMMAND
                        if inPuTMsG.strip().startswith('x122809569 '):
                            print('Processing x122809569 command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "x122809569 <message>\n"
                                        "Example: x122809569 Nivashini"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(1):
                                        color = get_random_color()  # random color from your list
                                        colored_message = f"{get_random_color()}[b][c]{user_message}"  # correct format
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #TEAM SPAM MESSAGE COMMAND
                        if inPuTMsG.strip().startswith('x1228095690 '):
                            print('Processing x122809569 command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "x122809569 <message>\n"
                                        "Example: x122809569 Nivashini"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()

                                    for _ in range(1):
                                        color = get_random_color()  # random color from your list
                                        colored_message = f"{get_random_color()}[b][c]{user_message}"  # correct format
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #GALI SPAM MESSAGE 
                        if inPuTMsG.strip().startswith('troll '):
                            print('Processing troll command')

                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)

                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]❌ ERROR! Usage:\n"
                                        "troll <name>\n"
                                        "Example: troll comedian"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()

                                    messages = [
                                        "{Name} oda confidence paatha NASA kuda rocket launch cancel pannidum",
                                        "{Name} oda ideas ellam draft la irundha nalla irukum",
                                        "{Name} level ku reach aaganum na patience illa, comedy dhaan venum",
                                        "{Name} serious ah pesinaalum background la comedy music kekum",
                                        "{Name} brain use panna try pannanga… but loading dhaan......",
                                        "{Name} oda plan ellam start aagum… finish aagathu",
                                        "{Name} serious ah irundhaalum comedy piece dhaan",
                                        "{Name} oda thinking speed paatha buffering symbol kuda fast ah theriyudhu",
                                        "{Name} ah paatha doubt varudhu… idhu original ah illa trial version ah",
                                        "{Name} ah nambi plan pannina… game over",
                                        "{Name} oda life story… skip ad panna kooda worth illa",
                                        "{Name} oda decisions paatha mistake kuda insult aagum",
                                        "{Name} ku advice kudutha… return gift confusion dhaan",
                                        "{Name} serious ah pesumbodhu kooda… side la comedy subtitles varudhu ",
                                        "{Name} pesina apram… Google kuda doubt aagudhu",
                                        "{Name} idea launch speed super… but finish line reach aaganum na Google Maps kuda reroute aagudhu",
                                        "{Name} explanation start panna first line okay… second line twist… third line la ellarum lost "
            ]

                                    # Send each message one by one with random color
                                    for msg in messages:
                                        colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.upper())}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)

                            except Exception as e:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                #INSTA USERNAME TO INFO-/ig
                        if inPuTMsG.strip().startswith('/ig '):
                            print('Processing insta command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ig <username>\nExample: /ig virat.kohli\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                
        
        # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    insta_result = await loop.run_in_executor(executor, send_insta_info, target_username)
        
                                await safe_send_message(response.Data.chat_type, insta_result, uid, chat_id, key, iv)
                                #GET PLAYER BIO-/bio
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /bio <uid>\nExample: /bio 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    bio_result = await loop.run_in_executor(executor, get_player_bio, target_uid)

                                await safe_send_message(response.Data.chat_type, f"{bio_result}", uid, chat_id, key, iv)
                                
                        if inPuTMsG.strip().startswith('/ghost '):
                            print('Processing ghost command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ghost <Teamcode>\nExample: /Teamcode 4368569\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                teamcode = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ghost_result = await loop.run_in_executor(executor, get_ghost_join, teamcode)

                                await safe_send_message(response.Data.chat_type, f"{ghost_result}", uid, chat_id, key, iv)
                                
                                
                        if inPuTMsG.strip().startswith('/info '):
                            print('Processing bio command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /info <uid>\nExample: /info 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    info_result = await loop.run_in_executor(executor, get_player_info, target_uid)

                                await safe_send_message(response.Data.chat_type, f"{info_result}", uid, chat_id, key, iv)
                                await asyncio.sleep(0)
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    guild_result = await loop.run_in_executor(executor, get_guild_info, target_uid)

                                await safe_send_message(response.Data.chat_type, guild_result, uid, chat_id, key, iv)
                                #GET PLAYER Name-/name
                        if inPuTMsG.strip().startswith('/name '):
                            print('Processing nickname command in any chat type')

                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /name <uid>\nExample: /name 4368569733\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    name_result = await loop.run_in_executor(executor, get_player_name, target_uid)

                                await safe_send_message(response.Data.chat_type, f"{name_result}", uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('hi ami'):
                                sir = response.Data.uid

                                # Use ThreadPoolExecutor to avoid blocking the async loop
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    name_result = await loop.run_in_executor(executor, get_player_name, sir)
                                    msg_result = f"Hello[B][C]{get_random_color()} {name_result}"

                                await safe_send_message(response.Data.chat_type, msg_result, uid, chat_id, key, iv)

                        # QUICK EMOTE ATTACK COMMAND - /quick [team_code] [emote_id] [target_uid?]
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
    
                            parts = inPuTMsG.strip().split()
    
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n[00FF00]/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n[00FF00]/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
        
                                # Set default values
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)  # Default: Sender's UID
        
                                # Parse optional parameters
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
        
                                # Determine target name for message
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
        
                                initial_message = f"[B][C][FFFF00]⚡ QUICK EMOTE ATTACK!\n\n[FFFFFF]🎯 Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n[FFFFFF]⏱️ Estimated: [00FF00]2 seconds\n\n[FFFF00]Executing sequence...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
        
                                try:
                                    # Try regular method first
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
            
                                    if success:
                                        success_message = f"[B][C][00FF00]✅ QUICK ATTACK SUCCESS!\n\n[FFFFFF]🏷️ Team: [00FF00]{team_code}\n[FFFFFF]🎭 Emote: [00FF00]{emote_id}\n[FFFFFF]👤 Target: [00FF00]{target_name}\n\n[00FF00]Bot joined → emoted → left! ✅\n"
                                    else:
                                        success_message = f"[B][C][FF0000]❌ Regular attack failed: {result}\n"
                                    
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print("failed")
            
            
                        # Invite Command - /inv (creates 5-player group and sends request)
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Processing invite command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /inv (uid)\nExample: /inv 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"\nSend invite to {xMsGFixinG(target_uid)}\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Fast squad creation and invite for 5 players
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                    
                                    C = await cHSq(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                    await asyncio.sleep(0.3)
                                    
                                    V = await SEnd_InV(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)
                                    
                                    # SUCCESS MESSAGE
                                    success_message = f"[B][C][00FF00]✅ SUCCESS! 5-Player Group invitation sent successfully to {target_uid}!\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending invite: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG == "/6":
                            # Process /6 command - Create 6 player group
                            initial_message = f"[B][C]{get_random_color()}Accept 6-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                           
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(6, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            
                        if inPuTMsG == "/2":
                            # Process /2 command - Create 2 player group
                            initial_message = f"[B][C]{get_random_color()}Accept 2-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                           
                            
                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(2, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)

                        if inPuTMsG == "/4":
                            # Process /4 command - Create 4 player group
                            initial_message = f"[B][C]{get_random_color()}Accept 4-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                           
                            
                            # Fast squad creation and invite for 4 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(4, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                        if inPuTMsG == "/3":
                            # Process /3 command - Create 3 player group
                            initial_message = f"[B][C]{get_random_color()}Accept 3-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                           
                            
                            # Fast squad creation and invite for 6 players
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(3, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, int(uid), key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)

                        if inPuTMsG.strip().startswith('/rmsg'):
                            print('Processing room message command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /roommsg (room_id) (message)\nExample: /roommsg 489775386 Hello room!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = " ".join(parts[2:])
        
                                initial_msg = f"[B][C][00FF00]📢 Sending to room {room_id}: {message}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Get bot UID
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 13699776666
            
                                    # Send room chat using leaked packet structure
                                    room_chat_packet = await send_room_chat_enhanced(message, room_id, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', room_chat_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Message sent to room {room_id}!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"✅ Room message sent to {room_id}: {message}")
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG == "/5":
                          try:
                            # Process /5 command in any chat type
                            initial_message = f"[B][C]{get_random_color()}Accept 5-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            
                            # Fast squad creation and invite
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            
                            C = await cHSq(5, response.Data.uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            
                            V = await SEnd_InV(5, response.Data.uid, key, iv, region)
                            await asyncio.sleep(0.3)  # Reduced delay
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(5)  # Reduced from 3 seconds
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                          except Exception as e:
                              print("Error For Group Creation")

                        if inPuTMsG.strip() == "/admin":
                            # Process /admin command in any chat type
                            admin_message = """\n\n\n[B][C][FB0364]╭[D21A92]─[BC26AB]╮\n[FF7244]│[FE4250]◯[C81F9C]֯│ [ffffff][/b]@[i]ft_rosie._ㅤ\n[/i][b][FDC92B]╰[FF7640]─[F5066B]╯\n\n\n"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == "/evoid":
                            # Process /admin command in any chat type
                            id_message = """[C][B][FFD700]⚡ [00ffff]EVOLUTION EMOTE IDS [FFD700]⚡[ffffff]
                            
                            
1 : [66FF00]Ak[FFFFFF]

2 : [66FF00]Scar[FFFFFF]

3 : [66FF00]1st MP40[FFFFFF]

4 : [66FF00]1st M1014[FFFFFF]

5 : [66FF00]XM8[FFFFFF]

6 : [66FF00]UMP[FFFFFF]

7 : [66FF00]Famas[FFFFFF]

8 : [66FF00]MP5[FFFFFF]

9 : [66FF00]M1887[FFFFFF]

10 : [66FF00]M4A1[FFFFFF]

11 : [66FF00]Fist[FFFFFF]

12 : [66FF00]AN94[FFFFFF]

13 : [66FF00]Thompson[FFFFFF]

14 : [66FF00]2nd M1014[FFFFFF]

15 : [66FF00]2nd MP40[FFFFFF]

16 : [66FF00]Groza[FFFFFF]

17 : [66FF00]Woodpecker[FFFFFF]

18 : [66FF00]Parafal[FFFFFF]

19 : [66FF00]P90[FFFFFF]

20 : [66FF00]G18[FFFFFF]

21 : [66FF00]M60

"""
                            await safe_send_message(response.Data.chat_type, id_message, uid, chat_id, key, iv)
                        # Add this with your other command handlers in the TcPChaT function
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Processing multi-account join request')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /multijoin (target_uid)\nExample: /multijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                initial_msg = f"[B][C][00FF00]🚀 Starting multi-join attack on {target_uid}...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Try the fake multi-account method (more reliable)
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
            
                                    if success_count > 0:
                                        result_msg = f"""
[B][C][00FF00]✅ MULTI-JOIN ATTACK COMPLETED!

🎯 Target: {target_uid}
✅ Successful Requests: {success_count}
📊 Total Attempts: {total_attempts}
⚡ Different squad variations sent!

💡 Check your game for join requests!
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]❌ All join requests failed! Check bot connection.\n"
            
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Multi-join error: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

           
                        if inPuTMsG.strip().startswith('/fastmultijoin'):
                            print('Processing fast multi-account join spam')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /fastmultijoin (uid)\nExample: /fastmultijoin 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Load accounts
                                accounts_data = load_accounts()
                                if not accounts_data:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! No accounts found!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                
                                initial_msg = f"[B][C][00FF00]⚡ FAST MULTI-ACCOUNT JOIN SPAM!\n🎯 Target: {target_uid}\n👥 Accounts: {len(accounts_data)}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    join_count = 0
                                    # Send join requests rapidly from all accounts
                                    for uid, password in accounts_data.items():
                                        try:
                                            # Use your existing join request function
                                            join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            join_count += 1
                                            print(f"✅ Fast join from account {uid}")
                    
                                            # Very short delay
                                            await asyncio.sleep(0.1)
                    
                                        except Exception as e:
                                            print(f"❌ Fast join failed for {uid}: {e}")
                                            continue
            
                                    success_msg = f"[B][C][00FF00]✅ FAST MULTI-JOIN COMPLETED!\n🎯 Target: {target_uid}\n✅ Successful: {join_count}/{len(accounts_data)}\n⚡ Speed: Ultra fast\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR in fast multi-join: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
           

                        # Update the command handler
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Processing reject spam command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /reject (target_uid)\nExample: /reject 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing reject spam
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Send start message
                                start_msg = f"[B][C][1E90FF]🌀 Started Reject Spam on: {target_uid}\n🌀 Packets: 150 each type\n🌀 Interval: 0.2 seconds\n"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
        
                                # Start reject spam in background
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
        
                                # Wait for completion in background and send completion message
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))


                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C][00FF00]✅ Reject spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ No active reject spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                
                                                    
                                                                        
                        # In your command handler where you call Room_Spam:
                        if inPuTMsG.strip().startswith('/rspm'):
                            print('Processing advanced room spam command')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /room (uid)\nExample: /rspm 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                room_id = parts[2]
        
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Please write a valid player ID!\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
        
                                # Send initial message
                                initial_msg = f"[B][C][00FF00]Working on room spam....."
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                await asyncio.sleep(2)
                                if fun_rspam_task and not fun_rspam_task.done():
                                  fun_rspam_running = False
                                  fun_rspam_task.cancel()
                                  await asyncio.sleep(1)
                                fun_rspam_running = True
                                fun_rspam_task = asyncio.create_task(fun_room_spam(target_uid, room_id, "Nivashini", key, iv))
                                successful_msg = f"[b][c][00ff00]Spam Started"
                                await safe_send_message(response.Data.chat_type, successful_msg, uid, chat_id, key, iv)
                                
                        if inPuTMsG.strip() == '/srspm':
                            if fun_rspam_task and not fun_rspam_task.done():
                                  fun_rspam_running = False
                                  fun_rspam_task.cancel()
                                  stop_msg = f"[B][C][00FF00]Room Spam Stopped Successfully!\n"
                                  await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No Active Room Spam To Stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)                                
                                
                                    
                                    
                        # Individual command handlers for /s1 to /s8
                        if inPuTMsG.strip().startswith('/s1 '):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
    
                        if inPuTMsG.strip().startswith('/s2 '):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s3 '):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s4 '):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/s5 '):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)

                        if inPuTMsG.strip().startswith('/spmj '):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]❌ Usage: /spmj <uid>\nExample: /spmj 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                total_requests = 10  # total join requests
                                sequence = ['s1', 's2', 's3', 's4', 's5']  # all badge commands

                                # Send initial consolidated message
                                initial_msg = f"[B][C][1E90FF]🌀 Request received! Preparing to spam {target_uid} with all badges...\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)

                                count = 0
                                while count < total_requests:
                                    for cmd in sequence:
                                        if count >= total_requests:
                                            break
                                        # Build a fake command string like "/s1 123456789"
                                        fake_command = f"/{cmd} {target_uid}"
                                        await handle_badge_commander(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        await asyncio.sleep(0.5)
                                        count += 1

                                # Success message after all 30 requests
                                success_msg = f"[B][C][00FF00]✅ Successfully sent {total_requests} Join Requests!\n🎯 Target: {target_uid}\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)                                    
                                                                                                     
                        if inPuTMsG.strip().startswith('/rjoin'):
                            print('Processing custom room join command')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /rjoin (room_id) (password)\nExample: /rjoin 123456 0000\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
        
                                initial_msg = f"[B][C][00FF00]🚀 Joining custom room...\n🏠 Room: {room_id}\n🔑 Password: {room_password}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Join the custom room
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Joined custom room {room_id}!\n🤖 Bot is now in room chat!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to join room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Processing custom room creation')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ Usage: /createroom (room_name) (password) [players=4]\nExample: /createroom BOTROOM 0000 4\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
        
                                initial_msg = f"[B][C][00FF00]🏠 Creating custom room...\n📛 Name: {room_name}\n🔑 Password: {room_password}\n👥 Max Players: {max_players}\n"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
        
                                try:
                                    # Create custom room
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
            
                                    success_msg = f"[B][C][00FF00]✅ Custom room created!\n🏠 Room: {room_name}\n🔑 Password: {room_password}\n👥 Max: {max_players}\n🤖 Bot is now hosting!\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ Failed to create room: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)                                                                                                                                                                                                               
                                                
                                              
                                                                                          # FIXED JOIN COMMAND
                        if inPuTMsG.startswith('/join '):
                            # Process /join command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /join (team_code)\nExample: /join ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
        
                                
        
                                try:
                                    # Try using the regular join method first
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
            
                                    # Wait a bit for the join to complete
                                    await asyncio.sleep(0.1)
            
                                    # DUAL RINGS EMOTE - BOTH SENDER AND BOT
                                    
            
                                    # SUCCESS MESSAGE
                                    success_message = f"\nJoin Success\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
            
                                except Exception as e:
                                    print(f"Team join faild")
                                    # If regular join fails, try ghost join
                        if inPuTMsG.strip().startswith('/bundle'):
                            print('Processing bundle command')
    
                            parts = inPuTMsG.strip().split()
                            
                            if inPuTMsG.strip() == ("/bundle"):
                                # Show available bundles
                                bundle_list = """[C][B][FFD700]      ⚡ [00ffff]BUNDLE IDS [FFD700]⚡[ffffff]
                            
                            
1 : [66FF00]Rampage[FFFFFF]

2 : [66FF00]Cannibal Havoc[FFFFFF]

3 : [66FF00]Devil Trigger[FFFFFF]

4 : [66FF00]Scorpio[FFFFFF]

5 : [66FF00]Frostfire[FFFFFF]

6 : [66FF00]Last Paradox[FFFFFF]

7 : [66FF00]Naruto's Ascent[FFFFFF]

8 : [66FF00]Aurora[FFFFFF]

9 : [66FF00]Midnight Ace[FFFFFF]

10 : [66FF00]Itachi[FFFFFF]

11 : [66FF00]Dreamspace[FFFFFF]"""
                                await safe_send_message(response.Data.chat_type, bundle_list, uid, chat_id, key, iv)
                            else:
                                bundle = parts[1]
                                try:
                                    # Create bundle packet
                                    bundle_packet = await bundle_packet_async(bundle, key, iv, region)
            
                                    if bundle_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bundle_packet)
                                        success_msg = f"Bundle Changed"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"Failed to create bundle packet!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                
                                except Exception as e:
                                    error_msg = f"❌ Error sending bundle: {str(e)[:50]}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    
                        if inPuTMsG.startswith('/kick '):
                            # Process /join command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"typo mistake?"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                if is_admin(uid):
                                   try:
                                    EM = await KickTarget(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                    await asyncio.sleep(0.1)
                                    success_message = f"\nPlayer Kicked\n"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                   except Exception as e:
                                    print(f"Kick faild")
                                else:
                                  age = f"\nAdmin Only Can Kick\n"
                                  await safe_send_message(response.Data.chat_type, age, uid, chat_id, key, iv)
                
                        if inPuTMsG.strip().startswith('/pei'):
                            # Process /ghost command in any chat type
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /ghost (team_code)\nExample: /ghost ABC123\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}\nGhost joining squad with code: {CodE}...\n"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                
                                try:
                                    # Get bot's UID from global context or login data
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                    
                                    ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                        success_message = f"[B][C][00FF00]✅ SUCCESS! Ghost joined squad with code: {CodE}!\n"
                                        await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Failed to create ghost join packet.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Ghost join failed: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW LAG COMMAND
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Processing lag command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"\n\nError!\nUse: /lag (team_code)\nExample: /lag ABC123\n\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                
                                # Stop any existing lag task
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)
                                
                                # Start new lag task
                                lag_running = True
                                lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                
                                # SUCCESS MESSAGE
                                success_msg = f"\nlag Started\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                await asyncio.sleep(1)
                                lag_idea = f"\n\nIf You Want to Stop Lag Cycle Just Send Me\n/slag\n\n"
                                await safe_send_message(response.Data.chat_type, lag_idea, uid, chat_id, key, iv)

                        # STOP LAG COMMAND
                        if inPuTMsG == '/slag':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"\nLag Stopped\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"\nNo Active lag To Stop\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG == '/fun':
                                fun_group_running = True
                                fun_group_task = asyncio.create_task(fun_group_change(uid, key, iv, region))
                                
                                # SUCCESS MESSAGE
                                success_msg = f"\n\nFun Started!\n\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # STOP LAG COMMAND
                        if inPuTMsG == '/sfun':
                            if fun_group_task and not fun_group_task.done():
                                fun_group_running = False
                                fun_group_task.cancel()
                                success_msg = f"\n\nFun Stopped!\n\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"No Active Fun Task To Stop\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG == 'bye':
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                            joining_team = False
                            success_message = f"\nLeave Success\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                            
                        if inPuTMsG.startswith('/bug '):
                             for i in range(30):
                               lag = await LagSquad(key,iv)
                               await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , lag)
                               await asyncio.sleep(0.05)
                             success_message = f"\nlag Success\n"
                             await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/start'):
                            # Process /start command in any chat type
                            initial_message = f"[B][C]{get_random_color()}\nStarting match...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            
                            # SUCCESS MESSAGE
                            success_message = f"[B][C][00FF00]✅ SUCCESS! Match starting command sent!\n"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/title'):
                            # Process /title command in any chat type
                            parts = inPuTMsG.strip().split()
    
                            # Check if bot is in a team
              
                            initial_message = f"[B][C]{get_random_color()}\nSending title to current team...\n"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            try:
                                # Send title packet
                               
                                title_packet = await send_title_msg(self, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', title_packet)
        
                                # SUCCESS MESSAGE
                                success_message = f"[B][C][00FF00]✅ SUCCESS! Title sent to current team!\n"
                                await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
        
                            except Exception as e:
                                print(f"Title send failed: {e}")
                                error_msg = f"[B][C][FF0000]❌ ERROR! Failed to send title: {str(e)}\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Emote command - works in all chat types
                        if inPuTMsG.strip().startswith('/e '):
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /e (uid) (emote_id)\nExample: /e 123456789 909000001\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                                
                            initial_message = f'[B][C]{get_random_color()}\nSending emote to target...\n'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)

                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []

                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])  # Last part is emote ID

                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Error parsing emote command: {e}")
                                s = True

                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Emote {idT} sent to {len(target_uids)} player(s)!\nTargets: {', '.join(map(str, target_uids))}\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR sending emote: {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Invalid UID format. Usage: /e (uid) (emote_id)\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                

                        # EVO CYCLE START COMMAND - /dance
                        if inPuTMsG.strip().startswith('/dance'):
                            print('Processing evo cycle start command in any chat type')
    
                            parts = inPuTMsG.strip().split()
                            uids = []
    
                            # Always use the sender's UID (the person who typed /dance)
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
    
                            # Optional: Also allow specifying additional UIDs
                            if len(parts) > 1:
                                for part in parts[1:]:  # Skip the first part which is "/dance"
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:  # UIDs are usually 7+ digits
                                        uids.append(part)
                                        print(f"Added additional UID: {part}")

                            # Stop any existing evo cycle
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
    
                            # Start new evo cycle
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
    
                            # SUCCESS MESSAGE
                            if len(uids) == 1:
                                success_msg = f"\nLet's Dance\n"
                            else:
                                success_msg = f"\nLet's Dance You And Your Friend {len(uids)-1}Players\n"
    
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            await asyncio.sleep(1)
                            idea_msg = f"\n\nIf You Want to Stop Dancing Cycle Just Send Me\n/sdance\n\n"
                            await safe_send_message(response.Data.chat_type, idea_msg, uid, chat_id, key, iv)
                            print(f"Started evolution emote cycle for UIDs: {uids}")
                        
                        # EVO CYCLE STOP COMMAND - /sdance
                        if inPuTMsG.strip() == '/sdance':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"\nDancing Emote Cycle Stopped\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Evolution emote cycle stopped by command")
                            else:
                                error_msg = f"\nNo Active Dancing Emote Cycle To Stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Fast emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/f '):
                            print('Processing fast emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /f uid1 [uid2] [uid3] [uid4] emoteid\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and emoteid
                                uids = []
                                emote_id = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:  # Assuming UIDs are longer than 3 digits
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /f uid1 [uid2] [uid3] [uid4] emoteid\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    # Stop any existing fast spam
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    
                                    # Start new fast spam
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    
                                    # SUCCESS MESSAGE
                                    success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times\n"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Custom emote spam command - works in all chat types
                        if inPuTMsG.strip().startswith('/c '):
                            print('Processing custom emote spam in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /p (uid) (emote_id) (times)\nExample: /p 123456789 909000001 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
                                    
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Times must be greater than 0!\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                                    else:
                                        # Stop any existing custom spam
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                                        
                                        # Start new custom spam
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        
                                        # SUCCESS MESSAGE
                                        success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom emote spam started!\nTarget: {target_uid}\nEmote: {emote_id}\nTimes: {times}\n"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                        
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Usage: /p (uid) (emote_id) (times)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! {str(e)}\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Spam request command - works in all chat types
                        if inPuTMsG.strip().startswith('/spmi '):
                            print('Processing spam invite with cosmetics')
    
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ Usage: /spmi (uid)\nExample: /spmi 123456789\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
        
                                # Stop any existing spam request
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
        
                                # Start new spam request WITH COSMETICS
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop(target_uid, key, iv, region))
        
                                # SUCCESS MESSAGE
                                success_msg = f"[B][C][00FF00]✅ COSMETIC SPAM STARTED!\n🎯 Target: {target_uid}\n📦 Requests: 30\n🎭 Features: V-Badges + Cosmetics\n⚡ Each invite has different cosmetics!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)

                        # Stop spam request command - works in all chat types
                        if inPuTMsG.strip() == '/sspmi':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Spam request stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active spam request to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO COMMANDS
                        if inPuTMsG.strip().startswith('/evo '):
                            print('Processing evo command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evo 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evo uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}\nSending evolution emote {number_int}...\n"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            
                                            if success:
                                                success_msg = f"[B][C][00FF00]✅ SUCCESS! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]❌ ERROR! {result_msg}\n"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        if inPuTMsG.strip().startswith('/evof '):
                            print('Processing evo_fast command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evof uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /evof 123456789 1\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids and number
                                uids = []
                                number = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number should be 1-21 (1 or 2 digits)
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evof uid1 [uid2] [uid3] [uid4] number(1-21)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            # Stop any existing evo_fast spam
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_fast spam
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number format! Use 1-21 only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # NEW EVO_CUSTOM COMMAND
                        if inPuTMsG.strip().startswith('/evoc '):
                            print('Processing evo_c command in any chat type')
                            
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]❌ ERROR! Usage: /evoc uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /evoc 123456789 1 10\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                # Parse uids, number, and time
                                uids = []
                                number = None
                                time_val = None
                                
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:  # Number or time should be 1-100 (1, 2, or 3 digits)
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                
                                # If we still don't have time_val, try to get it from the last part
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        # Remove time_val from uids if it was added by mistake
                                        if time_val in uids:
                                            uids.remove(time_val)
                                
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]❌ ERROR! Invalid format! Usage: /evoc uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\n"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]❌ ERROR! Number must be between 1-21 only!\n"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        
                                        else:
                                            # Stop any existing evo_custom spam
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            
                                            # Start new evo_custom spam
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            
                                            # SUCCESS MESSAGE
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C][00FF00]✅ SUCCESS! Custom evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nRepeat: {time_int} times\nInterval: 0.1 seconds\n"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]❌ ERROR! Invalid number/time format! Use numbers only.\n"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_fast spam command
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution fast spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution fast spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

                        # Stop evo_custom spam command
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C][00FF00]✅ SUCCESS! Evolution custom spam stopped successfully!\n"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]❌ ERROR! No active evolution custom spam to stop!\n"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)

# IMPROVED TREE-STYLE HELP MENU SYSTEM (Commands in their original menus) 🌳
                        if inPuTMsG.strip().lower() in ("help", "/help", "menu", "/menu", "commands"):
                            print(f"Help command detected from UID: {uid} in chat type: {response.Data.chat_type}")

                            # Header
                            header = f"[b][c][ff99ff]Welcome To Nivashini's Bot\n\n[B][C][FB0364]╭[D21A92]─[BC26AB]╮\n[FF7244]│[FE4250]◯[C81F9C]֯│ [ffffff][/b]@[i]ft_rosie._ㅤ\n[/i][b][FDC92B]╰[FF7640]─[F5066B]╯\n"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(4)

                            # ───── Group Commands ─────
                            group_commands = """[C][B]    [FFD700]⚡ [00FFFF]GROUP COMMANDS [FFD700]⚡[FFFFFF]
                            

├─ Create 2-Player Group
│  └─ [66FF00]/2[FFFFFF]                            
├─ Create 3-Player Group
│  └─ [66FF00]/3[FFFFFF]
├─ Create 4-Player Group
│  └─ [66FF00]/4[FFFFFF]
├─ Create 5-Player Group
│  └─ [66FF00]/5[FFFFFF]
├─ Create 6-Player Group
│  └─ [66FF00]/6[FFFFFF]
├─ Invite Player
│  └─ [66FF00]/inv [uid][FFFFFF]
├─ Join Team
│  └─ [66FF00]/join [team_code][FFFFFF]
├─ Leave Group
│  └─ [66FF00]bye[FFFFFF]
└─ Start Match
       └─ [66FF00]/start
"""
                            await safe_send_message(response.Data.chat_type, group_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Advanced Commands ─────
                            advanced_commands = """[C][B][FFD700]⚡[00ffff] ADVANCED COMMANDS [ffd700]⚡[ffffff]
                            

├─ 5,6 Member Lobby Change
│  └─ [66FF00]/fun[ffffff]
├─ Stop 5,6 Lobby Change
│  └─ [66FF00]/sfun[ffffff]                            
├─ Spam Invites (30x)
│  └─ [66FF00]/spmi [uid][FFFFFF]
├─ Stop Spam Invites
│  └─ [66FF00]/sspmi[FFFFFF]
├─ Lag Attack Team
│  └─ [66FF00]/lag [code][FFFFFF]
├─ Stop Lag Attack
│  └─ [66FF00]/slag[FFFFFF]
└─ Reject Spam
       └─ [66FF00]/reject [uid][FFFFFF]
"""
                            await safe_send_message(response.Data.chat_type, advanced_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Emote Commands ─────
                            emote_commands = """[C][B][FFD700]   ⚡ [00ffff]EMOTE COMMANDS [FFD700]⚡[ffffff]
                            
                            
├─ Get player info by uid
│  └─ [66FF00]/info [uid][ffffff]
├─ Get player bio by uid
│  └─ [66FF00]/bio [uid][ffffff]
├─ Get player name by uid
│  └─ [66FF00]/name [uid][ffffff]
├─ Send Single Emote
│  └─ [66FF00]/e [uids] [id][ffffff]
├─ Fast Emote (50x)
│  └─ [66FF00]/f [uids] [id][ffffff]
└─ Custom Emote (X times)
       └─ [66FF00]/c [uid] [id] [x]
"""
                            await safe_send_message(response.Data.chat_type, emote_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Evolution Emote Commands ─────
                            evo_commands = """[C][B][FFD700]      ⚡ [00ffff]EVOLUTION EMOTES [FFD700]⚡[ffffff]
                            

├─ Get Evo Emote Chart
│  └─ [66FF00]/evoid[ffffff]
├─ Send Evolution Emote
│  └─ [66FF00]/evo [uid] [1-21][ffffff]
├─ Fast Evo (50x)
│  └─ [66FF00]/evof [uid] [1-21][ffffff]
├─ Custom Evo (X times)
│  └─ [66FF00]/evoc [uid] [1-21] [x][ffffff]
├─ Auto Cycle All Evo Emotes
│  └─ [66FF00]/dance [uid][ffffff]
└─ Stop Evo Emote Cycle
       └─ [66FF00]/sdance
"""
                            await safe_send_message(response.Data.chat_type, evo_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── AI & Utility Commands ─────
                            ai_commands = """[C][B][FFD700]⚡ [00ffff]INFORMATION COMMANDS [FFD700]⚡[ffffff]
                            
                            
├─ Get Bundle Chart
│  └─ [66FF00]/bundle [ffffff]
├─ Change Bot Bundle
│  └─ [66FF00]/bundle [number][ffffff]
├─ Kick Someone 
│  └─ [66FF00]/kick [uid][ffffff]
└─ Admin Information
       └─ [66FF00]/admin
"""
                            await safe_send_message(response.Data.chat_type, ai_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            # ───── Badges Commands ─────
                            badge_commands = """[C][B][FFD700]   ⚡ [00ffff]BADGE JOIN REQUESTS [FFD700]⚡[ffffff]
                            
                            
├─ Join Req Craftland Badge
│  └─ [66FF00]/s1 [uid][ffffff]
├─ Join Req New V-Badge
│  └─ [66FF00]/s2 [uid][ffffff]
├─ Join Req Moderator Badge
│  └─ [66FF00]/s3 [uid][ffffff]
├─ Join Req Small V-Badge
│  └─ [66FF00]/s4 [uid][ffffff]
├─ Join Req Pro Badge
│  └─ [66FF00]/s5 [uid][ffffff]
└─ Join Req All Badge
       └─ [66FF00]/spmj [uid]
"""
                            await safe_send_message(response.Data.chat_type, badge_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)

                            
                            footer ="""[b][c]    [FFD700]          ⚡[00ffff]BOT INFO[FFD700] ⚡[ffffff]

Developer :: [66FF00]Nivashini[ffffff]
Developer ffid :: [66FF00]ᏞꜰㅤᎠꪮνꫀㅤʚĭɞ [ffffff]([66FF00]122🗿809🗿569[ffffff])
Status :: [66FF00]ONLINE[ffffff]
Version :: [66FF00]2.117.1
"""

    


                            await safe_send_message(response.Data.chat_type, footer, uid, chat_id, key, iv)
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)





async def MaiiiinE():
    Uid , Pw = '4210598764','D76B9581330C8899873F88B8CFCED603DD89B659F42F4E248975DC2C52612E61'
    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    print(f"Access Token = {access_token}")
    #open_id , access_token = 'ee97ddca18e47a3f739dbf9370a255b0' , 'd30b3fd1d3e72a82dc6f7b7230efd29940ea8dc64ef9e874cbfe4788afdb163e'
    if not open_id or not access_token: print("ErroR - InvaLid AccounT") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    # In the MaiiiinE function, find and comment out these print statements:
    print("🌐 Server connection established")

    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    print("🔐 Authentication successful")
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    print(f"Your Jwt ToKen = {ToKen}")
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin DaTa !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    #print(acc_name)
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))  
    await asyncio.gather(task1, task2)
    time.sleep(0.5)
    await ready_event.wait()
    await asyncio.sleep(1)
    print(render('NIVASHINI', colors=['white', 'green'], align='center'))
    print('')
    print("🤖 NIVASHINI BOT - ONLINE")
    print(f"🔹 UID: {TarGeT}")
    print(f"🔹 Name: {acc_name}")
    print(f"🔹 Status: 🟢 READY")
    


def handle_keyboard_interrupt(signum, frame):
    """Clean handling for Ctrl+C"""
    print("\n\n🛑 Bot shutdown requested...")
    print("👋 Thanks for using my bot")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    
async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot shutdown by user")
            print("👋 Thanks for using my bot!")
            break
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    asyncio.run(StarTinG())
