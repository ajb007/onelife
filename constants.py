ACTION_TIMEOUT             = 0

MALE                       = 0
FEMALE                     = 1

# server run_level constants
RUN_SERVER                 = 0      # continue through main loop
HARD_SHUTDOWN              = 1      # kill server NOW
FAST_SHUTDOWN              = 2      # just save the realm
SHUTDOWN                   = 3      # wait on threads, then save
LEISURE_SHUTDOWN           = 4      # wait until no one is logged on

# thread run_level constants
SIGNING_IN                = 0       # connection has no account
CHAR_SELECTION            = 1       # player needs a character
PLAY_GAME                 = 2       # in play
SAVE_AND_CONTINUE         = 3       # save char and ask to continue
SAVE_AND_EXIT             = 4       # save char and leave game
GO_AGAIN                  = 5       # save char and leave game
EXIT_THREAD               = 6       # leave the main loop
LEAVING_THREAD            = 7       # Final thread exit

# socket return values
S_NORM                    = 0       # socket returned data
S_CANCEL                  = 1       # player canceled selection
S_TIMEOUT                 = 2       # player ran out of time
S_ERROR                   = 3       # socket is closed

# tag types
T_REJECT                  = 0       # hang up on address ASAP
T_BAN                     = 1       # kick when character loaded, ban
T_SUICIDE                 = 2       # all loaded characters hari-kari
T_MUTE                    = 3       # player may not chat
T_PREFIX                  = 4       # add a prefix to the player
T_SUFFIX                  = 5       # add a suffix to the player

# tagged types
T_MACHINE                 = 0       # tag of a specific machine
T_ACCOUNT                 = 1       # tag of an account
T_ADDRESS                 = 2       # tag of an address
T_NETWORK                 = 3       # tag of an network

# hearing constants
HEAR_SELF                 = 0       # hear the channel you're in
HEAR_ONE                  = 1       # hear channel 1 -- apprentice
HEAR_ALL                  = 11      # hear all channels

# realm objects
ENERGY_VOID               = 0       # object is an energy void
CORPSE                    = 1       # object is a corpse
TREASURE_TROVE            = 2       # object is the treasure trove
HOLY_GRAIL                = 3       # object is the holy grail

# total number of things
NUM_MONSTERS              = 100     # monsters in the game
NUM_CHARS                 = 6       # number of character types
NUM_ITEMS                 = 7       # items in the shops

# event types
NULL_EVENT                = 0       # blank event
# immediate events
KICK_EVENT                = 1       # get off my game
TAG_EVENT                 = 2       # tag yourself
REQUEST_DETAIL_EVENT      = 3       # get player info
CONNECTION_DETAIL_EVENT   = 4       # another player's info
REQUEST_RECORD_EVENT      = 5       # get player info
PLAYER_RECORD_EVENT       = 6       # another player's info
ADD_PLAYER_EVENT          = 7       # add player info
REMOVE_PLAYER_EVENT       = 8       # remove player info
CHANGE_PLAYER_EVENT       = 9       # change player info
CHAT_EVENT                = 10      # chat message
REPRIMAND_EVENT           = 11      # Apprentices reprimand
UNTAG_EVENT               = 12      # remove a prefix or suffix
UNSUSPEND_EVENT           = 13      # resume player's game
GAME_MARKER               = 14      # only game events follow
# ASAP events
DEATH_EVENT               = 20      # player died
IT_COMBAT_EVENT           = 21      # enter interterminal-combat
EXPERIENCE_EVENT          = 23      # award the player experience
# tampering events
SUSPEND_EVENT             = 25      # stop player's game
CANTRIP_EVENT             = 26      # apprentice options
MODERATE_EVENT            = 27      # wizard options
ADMINISTRATE_EVENT        = 28      # administrative options
VALAR_EVENT               = 29      # become/lose valar
KING_EVENT                = 30      # become king
STEWARD_EVENT             = 31      # become steward
DETHRONE_EVENT            = 32      # lose king or steward
SEX_CHANGE_EVENT          = 34      # toggle player's sex
RELOCATE_EVENT            = 35      # order player to location
TRANSPORT_EVENT           = 36      # transport player
CURSE_EVENT               = 37      # curse player
SLAP_EVENT                = 38      # slap player
BLIND_EVENT               = 39      # blind player
BESTOW_EVENT              = 40      # king bestowed gold
SUMMON_EVENT              = 41      # summon monster for player
BLESS_EVENT               = 42
HEAL_EVENT                = 43
STRONG_NF_EVENT           = 44      # set the player's strength_nf flag
KNIGHT_EVENT              = 45      # this player has been knighted
DEGENERATE_EVENT          = 46
HELP_EVENT                = 47      # player is asking for information

# command events
COMMAND_EVENT             = 48      # the valar uses a power
SAVE_EVENT                = 49      # save the game and quit
MOVE_EVENT                = 50      # move the character
EXAMINE_EVENT             = 51      # examine the stats on a character
DECREE_EVENT              = 52      # make a decree
ENACT_EVENT               = 53      # the steward enacts something
LIST_PLAYER_EVENT         = 54      # list the players in the game
CLOAK_EVENT               = 55      # cloak/uncloak
TELEPORT_EVENT            = 56      # teleport player
INTERVENE_EVENT           = 57      # a council uses a power
REST_EVENT                = 58      # rest player
INFORMATION_EVENT         = 59      # go to information screen
FORCEAGE_EVENT            = 60      # forcefully age a player

# normal events
# events after this are destroyed on orphan
DESTROY_MARKER            = 69
ENERGY_VOID_EVENT         = 70      # create/hit energy void
TROVE_EVENT               = 71      # find the treasure trove
MONSTER_EVENT             = 72      # encounter monster
PLAGUE_EVENT              = 73      # hit with plague
MEDIC_EVENT               = 74      # encounter medic
GURU_EVENT                = 75      # encounter guru
TRADING_EVENT             = 76      # find a trading post
TREASURE_EVENT            = 77      # find treasure
VILLAGE_EVENT             = 78      # found a village or a volcano
TAX_EVENT                 = 79      # encounter tax collector

# other events
NATINC_EVENT              = 84      # restoration of natural stats
EQINC_EVENT               = 85      # restoration of equipment
CINC_EVENT                = 86      # restoration of currency
AGING_EVENT               = 87      # Age restore
ITEMINC_EVENT             = 88      # Restores items


# realm objects
# events after this are made realm objects on orphan
REALM_MARKER              = 90
CORPSE_EVENT              = 91      # find a corpse
GRAIL_EVENT               = 92      # find the holy grail
LAST_EVENT                = 93      # used to find bad events

# combat messages
IT_OPPONENT_BUSY          = 1      # currently on another combat
IT_REPORT                 = 2      # report in
IT_JUST_DIED              = 3      # player has just been killed
IT_JUST_LEFT              = 42     # player just left the game
IT_ATTACK                 = 4      # player is attacker
IT_DEFEND                 = 5      # player is defender
IT_MELEE                  = 6      # attacker meleed
IT_SKIRMISH               = 7      # attacker skirmished
IT_NICKED                 = 8      # attacker nicked
IT_EVADED                 = 9      # attacker evaded
IT_NO_EVADE               = 10     # attacker failed to evade
IT_LUCKOUT                = 11     # attacker lucked-out (luckouted?)
IT_NO_LUCKOUT             = 12     # attacker failed to luckout
IT_RING                   = 13     # attacker put on a ring
IT_NO_RING                = 14     # attacker failed to put on a ring
IT_ALL_OR_NOT             = 15     # attacker cast all or nothing
IT_NO_ALL_OR_NOT          = 16     # attacker blew all or nothing
IT_BOLT                   = 17     # attacker cast magic bolt
IT_NO_BOLT                = 18     # attacker blew magic bolt
IT_SHIELD                 = 19     # attacker cast force field
IT_NO_SHIELD              = 20     # attacker blew force field
IT_TRANSFORM              = 21     # attacker transformed defender
IT_NO_TRANSFORM           = 22     # attacker blew transform
IT_TRANSFORM_BACK         = 23     # attacker's transform backfired
IT_MIGHT                  = 24     # attacker cast increase might
IT_NO_MIGHT               = 25     # attacker blew increase might
IT_HASTE                  = 26     # attacker cast haste
IT_NO_HASTE               = 27     # attacker blew haste
IT_TRANSPORT              = 28     # attacker cast transport
IT_NO_TRANSPORT           = 29     # attacker blew transport
IT_TRANSPORT_BACK         = 30     # attacker's transport backfired
IT_PARALYZE               = 31     # attaker cast paralyze
IT_NO_PARALYZE            = 32     # attaker blew paralyze
IT_PASS                   = 33     # attacker passed the turn
IT_CONTINUE               = 34     # defender continues the battle
IT_CONCEDE                = 35     # defender surrenders
IT_DEFEAT                 = 36     # the sender stands defeated
IT_VICTORY                = 37     # the sender claims victory
IT_DONE                   = 38     # This is Kang, cease hostilities
IT_ECHO                   = 39     # tell me to attack
IT_ABANDON                = 40     # player quiting and saving self
IT_BORED                  = 41     # player quit after timeout
IT_WIZEVADE               = 43     # player used wiz powers to evade

# client->player packet headers
HANDSHAKE_PACKET          = 2      # used when connecting
CLOSE_CONNECTION_PACKET   = 3      # last message before close
PING_PACKET               = 4      # used for timeouts
ADD_PLAYER_PACKET         = 5      # add a player to the list
REMOVE_PLAYER_PACKET      = 6      # remove a player from the list
SHUTDOWN_PACKET           = 7      # the server is going down
ERROR_PACKET              = 8      # server has encountered an error
CLEAR_PACKET              = 10     # clears the message screen
WRITE_LINE_PACKET         = 11     # write a line on message screen
BUTTONS_PACKET            = 20     # use the interfaces buttons
FULL_BUTTONS_PACKET       = 21     # use buttons and compass
STRING_DIALOG_PACKET      = 22     # request a message response
COORDINATES_DIALOG_PACKET = 23     # request player coordinates
PLAYER_DIALOG_PACKET      = 24     # request a player name
PASSWORD_DIALOG_PACKET    = 25     # string dialog with hidden text
SCOREBOARD_DIALOG_PACKET  = 26     # pull up the scoreboard
DIALOG_PACKET             = 27     # okay dialog with next line
CHAT_PACKET               = 30     # chat message
ACTIVATE_CHAT_PACKET      = 31     # turn on the chat window
DEACTIVATE_CHAT_PACKET    = 32     # turn off the chat window
PLAYER_INFO_PACKET        = 33     # display a player's info
CONNECTION_DETAIL_PACKET  = 34     # display connection info
NAME_PACKET               = 40     # set the player's name
LOCATION_PACKET           = 41     # refresh the player's energy
ENERGY_PACKET             = 42     # refresh the player's energy
STRENGTH_PACKET           = 43     # refresh the player's strength
SPEED_PACKET              = 44     # refresh the player's speed
SHIELD_PACKET             = 45     # refresh the player's shield
SWORD_PACKET              = 46     # refresh the player's sword
QUICKSILVER_PACKET        = 47     # refresh the player's quicksilver
MANA_PACKET               = 48     # refresh the player's mana
LEVEL_PACKET              = 49     # refresh the player's level
GOLD_PACKET               = 50     # refresh the player's gold
GEMS_PACKET               = 51     # refresh the player's gems
CLOAK_PACKET              = 52     # refresh the player's cloak
BLESSING_PACKET           = 53     # refresh the player's blessing
CROWN_PACKET              = 54     # refresh the player's crowns
PALANTIR_PACKET           = 55     # refresh the player's palantir
RING_PACKET               = 56     # refresh the player's ring
VIRGIN_PACKET             = 57     # refresh the player's virgin

# player->client packet headers
C_RESPONSE_PACKET         = 1      # player feedback for game
C_CANCEL_PACKET           = 2      # player canceled question
C_PING_PACKET             = 3      # response to a ping
C_CHAT_PACKET             = 4      # chat message from player
C_EXAMINE_PACKET          = 5      # examine a player
C_ERROR_PACKET            = 6      # client is lost
C_SCOREBOARD_PACKET       = 7      # show the scoreboard

# locations within the realm
PL_REALM                  = 0      # normal coordinates
PL_THRONE                 = 1      # In the lord's chamber
PL_EDGE                   = 2      # On the edge of the realm
PL_VALHALLA               = 3      # In Valhalla
PL_PURGATORY              = 4      # In purgatory fighting

# size of many structures
#SZ_PLAYER sizeof(struct player_t) # size of player_t
#SZ_GAME sizeof(struct game_t) # size of game_t
#SZ_IT_COMBAT sizeof(struct it_combat_t) # size of it_combat_t
#SZ_PLAYER_DESC sizeof(struct player_desc_t) # size of player_desc_t
#SZ_PLAYER_SPEC sizeof(struct player_spec_t) # size of player_spec_t
#SZ_EVENT sizeof(struct event_t) # size of event_t
#SZ_REALM_STATE sizeof(struct realm_state_t) # size of realm_state_t
#SZ_REALM_OBJECT sizeof(struct realm_object_t) # size of realm_object_t
#SZ_SCOREBOARD sizeof(struct scoreboard_t) # size of scoreboard_t
#SZ_CLIENT sizeof(struct client_t) # size of client_t
#SZ_OPPONENT sizeof(struct opponent_t) # size of opponent_t
#SZ_BUTTON sizeof(struct button_t) # size of button_t
#SZ_ACCOUNT sizeof(struct account_t) # size of account_t
#SZ_LINKED_LIST sizeof(struct linked_list_t) # size of linked_list_t
#SZ_EXAMINE sizeof(struct examine_t)
#SZ_TAG sizeof(struct tag_t)
#SZ_TAGGED sizeof(struct tagged_t)
#SZ_TAGGED_LIST sizeof(struct tagged_list_t)
#SZ_NETWORK sizeof(struct network_t)
#SZ_CONNECTION sizeof(struct connection_t)
#SZ_HISTORY sizeof(struct history_t)
#SZ_HISTORY_LIST sizeof(struct history_list_t)
#SZ_DETAIL sizeof(struct detail_t)
#SZ_TAGGED_SORT sizeof(struct tagged_sort_t)

# string sizes
#SZ_IN_BUFFER  1024 # largest possible client message
#SZ_OUT_BUFFER  1024 # largest possible server message
#SZ_NAME   33 # player name field (incl. trailing null)
#MAX_NAME_LEN  16 # actual player name
#SZ_PASSWORD  16 # 128 bit MD5 hash of the password
#SZ_FROM   81 # ip or dns login (incl. null)
#SZ_MONSTER_NAME  49 # characters in monster names
#SZ_AREA   24 # name of player location
#SZ_HOW_DIED  78 # string describing character death
#SZ_CLASS_NAME  13 # longest class name
#define SZ_ITEMS  12 # longest shop item description
#define SZ_ERROR_MESSAGE 256 # max length of error message
#SZ_LINE   256 # length of one line on terminal
#SZ_LABEL  22 # length of interface button text
#SZ_NUMBER  25 # characters describing number
#SZ_CHAT   512 # largest chat message
#SZ_PACKET_TYPE  2 # maximum packet size
#SZ_SPEC   7 # 5 chars, newline and null

# possible errors
MALLOC_ERROR               = 1001
DATA_FILE_ERROR            = 1002
MONSTER_FILE_ERROR         = 1003
CHARACTER_FILE_ERROR       = 1004
CHARSTATS_FILE_ERROR       = 1004
SHOPITEMS_FILE_ERROR       = 1004
SCOREBOARD_FILE_ERROR      = 1005
CHAT_LOG_FILE_ERROR        = 1006
SOCKET_CREATE_ERROR        = 1007
SOCKET_BIND_ERROR          = 1008
SOCKET_LISTEN_ERROR        = 1009
SOCKET_SELECT_ERROR        = 1010
SOCKET_ACCEPT_ERROR        = 1011
MUTEX_INIT_ERROR           = 1012
MUTEX_DESTROY_ERROR        = 1013
MUTEX_LOCK_ERROR           = 1014
MUTEX_UNLOCK_ERROR         = 1015
PTHREAD_ATTR_ERROR         = 1016
PTHREAD_CREATE_ERROR       = 1017
GENERAL_EVENT_ERROR        = 1021
IMPOSSIBLE_EVENT_ERROR     = 1022
EVENT_ADDRESS_ERROR        = 1023
UNDEFINED_OBJECT_ERROR     = 1024
BATTLE_PHASE_ERROR         = 1025
DEFENDER_MESSAGE_ERROR     = 1026
BATTLE_MESSAGE_ERROR       = 1027
SEND_SOCKET_ERROR          = 1028
READ_SOCKET_ERROR          = 1029

# ring constants
R_NONE                     = 0      # no ring
R_NAZREG                   = 1      # regular Nazgul ring (expires)
R_DLREG                    = 2      # regular Dark Lord ring (does not expire)
R_BAD                      = 3      # bad ring
R_SPOILED                  = 4      # ring which has gone bad
R_YES                      = 5      # masked ring type

# constants for character types
C_MAGIC                    = 0      # magic user
C_FIGHTER                  = 1      # fighter
C_ELF                      = 2      # elf
C_DWARF                    = 3      # dwarf
C_HALFLING                 = 4      # halfling
C_EXPER                    = 5      # experimento

# constants for special character types
SC_NONE                    =  0    # not a special character
SC_KNIGHT                  =  1    # knight
SC_STEWARD                 =  2    # steward
SC_KING                    =  3    # king
SC_COUNCIL                 =  4    # council of the wise
SC_EXVALAR                 =  5    # past valar - now council
SC_VALAR                   =  6    # valar

    # means of death
K_OLD_AGE                  = 0     # old age
K_MONSTER                  = 1     # combat with monster
K_IT_COMBAT                = 2     # combat with another player
K_GHOSTBUSTERS             = 3     # lost connection
K_VAPORIZED                = 4     # vaporized by another player
K_RING                     = 5     # killed by a cursed ring
K_NO_ENERGY                = 6     # player ran out of energy
K_FELL_OFF                 = 7     # fell off the edge of the world
K_TRANSFORMED              = 8     # turned into another monster
K_SEGMENTATION             = 9     # bad internal error
K_SUICIDE                  = 10    # character did something bad
K_SQUISH                   = 11    # new wizard kill option
K_GREED                    = 12    # killed when carrying too much gold
K_FATIGUE                  = 13    # killed when speed = 0 from fatigue
K_SIN                      = 14    # goes to hell for too much evil

    # special monster constants
SM_RANDOM                  = -1    # pick a monster by normal means
SM_NONE                    = 0     # nothing special
SM_UNICORN                 = 1     # unicorn
SM_MODNAR                  = 2     # Modnar
SM_MIMIC                   = 3     # mimic
SM_DARKLORD                = 4     # Dark Lord
SM_LEANAN                  = 5     # Leanan-Sidhe
SM_SARUMAN                 = 6     # Saruman
SM_THAUMATURG              = 7     # thaumaturgist
SM_BALROG                  = 8     # balrog
SM_VORTEX                  = 9     # vortex
SM_NAZGUL                  = 10    # nazgul
SM_TIAMAT                  = 11    # Tiamat
SM_KOBOLD                  = 12    # kobold
SM_SHELOB                  = 13    # Shelob
SM_FAERIES                 = 14    # assorted faeries
SM_LAMPREY                 = 15    # lamprey
SM_SHRIEKER                = 16    # shrieker
SM_BONNACON                = 17    # bonnacon
SM_SMEAGOL                 = 18    # Smeagol
SM_SUCCUBUS                = 19    # succubus
SM_CERBERUS                = 20    # Cerberus
SM_UNGOLIANT               = 21    # Ungoliant
SM_JABBERWOCK              = 22    # jabberwock
SM_MORGOTH                 = 23    # Morgoth
SM_TROLL                   = 24    # troll
SM_WRAITH                  = 25    # wraith
SM_TITAN                   = 26    # titan
SM_IT_COMBAT               = 27    # fighting another player
SM_IDIOT                   = 28    # idiot
SM_SMURF                   = 29    # smurf
SM_MORON                   = 30    # moron

# encounter constants
MONSTER_RANDOM             = 0     # monster was wandering
MONSTER_CALL               = 1     # monster was hunted
MONSTER_FLOCKED            = 2     # another monster in herd
MONSTER_SHRIEKER           = 3     # called by shrieker
MONSTER_JABBERWOCK         = 4     # called by jabberwock
MONSTER_TRANSFORM          = 5     # monster was polymorphed
MONSTER_SUMMONED           = 6     # another player threw monster
MONSTER_SPECIFY            = 7     # player requested monster
MONSTER_PURGATORY          = 8     # encounter in purgatory

# scoreboard constants
SB_KEEP_ABOVE              = 1000  # below this level, delete chars
SB_KEEP_FOR                = 2592000 # seconds to keep low chars

# other constants
CORPSE_LIFE                = 2592000 # seconds corpses stay in game
KEEP_TIME                  = 2592000 # base secs to keep saved characters
NEWBIE_KEEP_TIME           = 259200  # base secs to keep saved characters
ACCOUNT_KEEP_TIME          = 7776000 # secs to keep accounts

# constants for altering coordinates
A_SPECIFIC                 = 0     # coordinates specified, non-TP
A_FORCED                   = 1     # coordinates specified, ignore Beyond
A_NEAR                     = 2     # coordinates not specified, move near
A_FAR                      = 3     # coordinates not specified, move far
A_TRANSPORT                = 4     # distant teleport
A_OUST                     = 5     # more distant teleport
A_BANISH                   = 6     # move player to beyond
A_TELEPORT                 = 7     # moved by teleport

# spell constants
P_HEAL                     = 0     # steward heals a player
P_CURE                     = 1     # council heals with poison cure
P_RESTORE                  = 2     # valar restores a character
P_CURSE                    = 0     # steward curse
P_EXECRATE                 = 1     # king's stronger curse
P_SMITE                    = 2     # valar decimates a character

# constants for spells
ML_ALLORNOTHING            = 0.0     # magic level for 'all or nothing'
MM_ALLORNOTHING            = 1.0     # mana used for 'all or nothing'
ML_MAGICBOLT               = 5.0     # magic level for 'magic bolt'
ML_INCRMIGHT               = 15.0    # magic level for 'increase might'
MM_INCRMIGHT               = 30.0    # mana used for 'increase might'
ML_HASTE                   = 25.0    # magic level for 'haste'
MM_HASTE                   = 35.0    # mana used for 'haste'
ML_FORCEFIELD              = 35.0    # magic level for 'force field'
MM_FORCEFIELD              = 60.0    # mana used for 'force field'
ML_XPORT                   = 45.0    # magic level for 'transport'
MM_XPORT                   = 100.0   # mana used for 'transport'
ML_PARALYZE                = 60.0    # magic level for 'paralyze'
MM_PARALYZE                = 125.0   # mana used for 'paralyze'
ML_XFORM                   = 75.0    # magic level for 'transform'
MM_XFORM                   = 150.0   # mana used for 'transform'
MM_SPECIFY                 = 1000.0  # mana used for 'specify'
ML_CLOAK                   = 20.0    # magic level for 'cloak'
MEL_CLOAK                  = 7.0     # experience level for 'cloak'
MM_CLOAK                   = 35.0    # mana used for 'cloak'
ML_TELEPORT                = 40.0    # magic level for 'teleport'
MEL_TELEPORT               = 12.0    # experience level for 'teleport'
MM_INTERVENE               = 3000.0  # mana used to 'intervene'
MM_COMMAND                 = 15000.0 # mana used to 'command'

# some miscellaneous constants
N_DAYSOLD                  = 30       # number of days old for purge
N_AGE                      = 750      # age to degenerate ratio
N_GEMVALUE                 = (1000.0) # number of gold pieces to gem ratio
N_FATIGUE                  = 50       # rounds of combat before -1 speed
N_SWORDPOWER               = .04      # percentage of strength swords increase

D_BEYOND                   = (1.0e6)       # distance to beyond point of no return
D_EXPER                    = (2000.0)      # distance experimentos are allowed
D_EDGE                     = (100000000.0) # edge of the world
D_CIRCLE                   = 125.0         # distance for each circle
STATELEN                   = 256           # random number state buffer
MIN_STEWARD                = 10.0          # minimum level for steward
MAX_STEWARD                = 200.0         # maximum level for steward
MIN_KING                   = 1000.0        # minimum level for king
MAX_KING                   = 2000.0        # maximum level for king

# hacking constants
H_SYSTEM                   = 0     # hacking the system
H_PASSWORDS                = 1     # hacking passwords
H_CONNECTIONS              = 2     # excessive connections
H_KILLING                  = 3     # killing rampage
H_PROFANITY                = 4     # using profanity
H_DISRESPECTFUL            = 5     # disrespectful to wizards
H_FLOOD                    = 6     # flooding chat
H_SPAM                     = 7     # spamming chat
H_WHIM                     = 8     # wizard's whim
