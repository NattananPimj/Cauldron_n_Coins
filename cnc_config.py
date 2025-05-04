import math


class Config:
    MUSIC_VOLUME = 0.1

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    MAP_WIDTH = 700
    MAP_HEIGHT = 400

    HERB_WIDTH = 200
    HERB_HEIGHT = 640

    INV_WIDTH = 200
    INV_HEIGHT = 600

    UI_WIDTH = 200
    UI_HEIGHT = 100

    FACTOR_x = 1 / 20  # each block
    MOVESPEED = 35  # the bigger, the slower

    COLOR = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (111, 171, 94),
        'brown': (54, 34, 25),
        'background': (212, 198, 169),
        'map': (212, 188, 159),
        'path': (94, 90, 78),
        'marks': (50, 50, 50),
        'inventory_bg': (150, 125, 90),
        'haggle1':(160, 135, 114),
        'haggle2':(163, 111, 88),
        'hagglebar': (217, 169, 147)
    }
    '''
    HERB PATTERN
        'name': ''
        'direction': '' # N E W S NE NW SE SW
        'func': '' # lamda x: func(x)
        'picture': ''
    '''

    POTION_POS = {
        "SWIFTNESS": (10, 650),
        "DEXITY": (400, 750),
        "MANA": (525, 450),
        "EXPLOSION": (800, 320),
        "FIRE": (450, 25),
        "LIGHT": (820, -50),
        "HEAL": (200, -150),
        "GROWTH": (250, -570),
        "STRENGTH": (15, -500),
        "STONE": (-400, -800),
        "SLEEP": (-500, -500),
        "SLOW": (-800, -205),
        "FROST": (-450, -70),
        "LIGHTNING": (-500, 350),
        "POISON": (-200, 200),
        "RAGE": (-500, 600)
    }

    POTION_info = {
        "SWIFTNESS": {
            'pic': '',
            'price': 0,
        },
        "DEXITY": {
            'pic': '',
            'price': 0,
        },
        "MANA": {
            'pic': '',
            'price': 0,
        },
        "EXPLOSION": {
            'pic': '',
            'price': 0,
        },
        "FIRE": {
            'pic': '',
            'price': 0,
        },
        "LIGHT": {
            'pic': '',
            'price': 0,
        },
        "HEAL": {
            'pic': '',
            'price': 0,
        },
        "GROWTH": {
            'pic': '',
            'price': 0,
        },
        "STRENGTH": {
            'pic': '',
            'price': 0,
        },
        "STONE": {
            'pic': '',
            'price': 0,
        },
        "SLEEP": {
            'pic': '',
            'price': 0,
        },
        "SLOW": {
            'pic': '',
            'price': 0,
        },
        "FROST": {
            'pic': '',
            'price': 0,
        },
        "LIGHTNING": {
            'pic': '',
            'price': 0,
        },
        "POISON": {
            'pic': '',
            'price': 0,
        },
        "RAGE": {
            'pic': '',
            'price': 0,
        }
    }

    # TODO: add name
    HERB_INFO = {
        '01': {
            'name': 'Moonveil',
            'funcX': lambda t: 5 * t + 10 * math.cos(t),
            'funcY': lambda t: 10 * math.sin(t),
            't': 75,
            'direction': 'E',
            'pic': 'H01.JPG'
        },

        '02': {
            'name': 'Emberroot',
            'funcX': lambda t: 5 * t,
            'funcY': lambda t: 10 * math.sin(t / 2),
            't': 50,
            'direction': 'E',
            'pic': 'H02.JPG'
        },

        '03': {
            'name': 'Whisperleaf',
            'funcX': lambda t: 5 * t,
            'funcY': lambda t: 10 * (t / 2 + abs((t / 2 % 5) - 2.5)),
            't': 40,
            'direction': 'NE',
            'pic': 'H03.JPG'
        },

        '04': {
            'name': 'Dragonbloom',
            'funcX': lambda t: (2 * t) + 10 * math.cos(t),
            'funcY': lambda t: (5 * t) + -15 * math.sin(t),
            't': 40,
            'direction': 'NE',
            'pic': 'H04.JPG'
        },

        '05': {
            'name': 'Gloamhollow',
            'funcX': lambda t: t / 2 * math.cos(t / 2),
            'funcY': lambda t: 5 * (t + math.cos(t)),
            't': 50,
            'direction': 'N',
            'pic': 'H05.JPG'
        },

        '06': {
            'name': 'Starroot',
            'funcX': lambda t: 10 * abs((t / 2 % 5) - 2.5),
            'funcY': lambda t: 5 * t,
            't': 40,
            'direction': 'N',
            'pic': 'H06.JPG'
        },

        '07': {
            'name': 'Eldersap',
            'funcX': lambda t: -5 * t,
            'funcY': lambda t: (2 * t) - 10 * abs(math.sin(t / 5)),
            't': int(15 * math.pi),
            'direction': 'NW',
            'pic': 'H07.JPG'
        },

        '08': {
            'name': 'Echolily',
            'funcX': lambda t: (-2 * t) - 10 * math.cos(t),
            'funcY': lambda t: (5 * t) + -15 * math.sin(t),
            't': 50,
            'direction': 'NW',
            'pic': 'H08.JPG'
        },

        '09': {
            'name': 'Stormsage',
            'funcX': lambda t: (-4 * t) - 10 * math.sin(t),
            'funcY': lambda t: 10 * math.cos(t / 2),
            't': 50,
            'direction': 'W',
            'pic': 'H09.JPG'
        },

        '10': {
            'name': 'Frostvine',
            'funcX': lambda t: -5 * t,
            'funcY': lambda t: 10 * math.sin(t / 2),
            't': 50,
            'direction': 'W',
            'pic': 'H10.JPG'
        },

        '11': {
            'name': 'Voidmint',
            'funcX': lambda t: 100 * math.sin(t / 8),
            'funcY': lambda t: 40 * math.cos(t / 8),
            't': 40,
            'direction': 'SW',
            'pic': 'H11.JPG'
        },

        '12': {
            'name': 'Dewshade',
            'funcX': lambda t: t,
            'funcX': lambda t: -5 * t,
            'funcY': lambda t: -10 * (t / 2 + abs((t / 2 % 5) - 2.5)),
            't': 40,
            'direction': 'SW',
            'pic': 'H12.JPG'
        },

        '13': {
            'name': 'Duskwort',
            'funcX': lambda t: 10 * math.sin(t / 2),
            'funcY': lambda t: 100 * math.cos(t / 10),
            't': 40,
            'direction': 'S',
            'pic': 'H13.JPG'
        },

        '14': {
            'name': 'Silvershroud',
            'funcX': lambda t: 20 * math.sin(t / 2),
            'funcY': lambda t: (-5 * t) + (10 * math.cos(t)),
            't': 50,
            'direction': 'S',
            'pic': 'H14.JPG'
        },

        '15': {
            'name': 'Mirththorn',
            'funcX': lambda t: (10 * math.sin(t / 3)) + t,
            'funcY': lambda t: 4 - (((t - 2) ** 2) / 25),
            't': 50,
            'direction': 'SE',
            'pic': 'H15.JPG'
        },

        '16': {
            'name': "Bird's heart" ,
            'funcX': lambda t: 5 * t + 10 * math.cos(t),
            'funcY': lambda t: -5 * t + 10 * math.sin(t),
            't': 50,
            'direction': 'SE',
            'pic': 'H16.JPG'
        },
    }
    RQ = {
        "SWIFTNESS": [
            "I need to outrun the wolves chasing me—got anything for that?",
            "A courier's life isn’t easy; I need to move faster. What do you have?",
            "I'm racing tomorrow—need a little extra edge.",
            "These old legs don't sprint like they used to; can you help?",
            "I have to deliver this urgent message before sundown—speed is vital!"
        ],
        "DEXITY": [
            "I keep dropping everything—can you make me more nimble?",
            "I’m a thief—um, I mean an artist—and I need to move silently!",
            "I'm training for acrobatics and need better balance.",
            "I fumble when handling delicate machinery. Can you fix that?",
            "I want to perfect my swordplay—any potions to enhance my moves?"
        ],
        "MANA": [
            "I’ve run out of magical reserves! Can you recharge me?",
            "My spells are sputtering. Do you have something for more power?",
            "I’m practicing a difficult incantation and need extra energy.",
            "The last battle drained me. I need my magic back.",
            "The mage tournament is tomorrow—I can’t compete without mana!"
        ],
        "EXPLOSION": [
            "I’ve got a boulder blocking my path. Can you help me blast it away?",
            "The enemy’s barricade is too strong. I need to create an entrance!",
            "My farm tools are stuck behind a rockslide—something to clear that?",
            "I heard a thief ran into the mountain caves. Any explosive potions?",
            "I want to impress someone by lighting up the sky—safely, of course."
        ],
        "FIRE": [
            "It's freezing! I need to start a fire but lost my flint.",
            "I’m camping and need to cook—any fire-starting potions?",
            "I need something to burn through these vines blocking my way.",
            "My forge went cold. Can you help reignite it?",
            "I want to scare off some bandits—anything fiery?"
        ],
        "LIGHT": [
            "The caves are too dark—I need to brighten my path!",
            "My lamp broke, and I’m afraid of the dark. Do you have light?",
            "I’m searching for something in the shadows—any glowing potions?",
            "The festival needs lanterns, but fire is dangerous. Anything safer?",
            "I need to guide my ship at night. Can I count on you?"
        ],
        "HEAL": [
            "My tummy hurts—do you have a potion for that?",
            "I tripped and hurt my leg. Can you help me heal quickly?",
            "My friend got scratched by a wild animal. Do you have a remedy?",
            "I’ve been feeling weak all week. Do you have something restorative?",
            "A warrior can’t fight with wounds—got a healing potion?"
        ],
        "GROWTH": [
            "My crops aren’t growing fast enough—any potions for plants?",
            "I want my herb garden to flourish before winter hits. Can you help?",
            "I broke my plant pot. Can your potion fix my flowers?",
            "I’m trying to restore a barren land. Do you have anything for that?",
            "My grandmother's flowers are wilting—do you have a growth remedy?",
        ],
        "STRENGTH": [
            "I need to move this fallen tree blocking the road—can you help me?",
            "The town’s water wheel is stuck, and I need extra muscle to fix it.",
            "I’m participating in the Strongman competition—anything to boost my power?",
            "A giant boulder is blocking my way—got a potion to help me break it?",
            "The fortress gates won’t budge. I need the strength to force them open!"

        ],
        "STONE": [
            "I need to endure a troll’s attack—got a potion for toughness?",
            "My path leads through thorny vines—can you protect me?",
            "There’s no armor for sale. Can a potion make my skin stone-like?",
            "We miners need something to block falling debris. Can you help?",
            "I’m sparring with the town blacksmith—anything for extra defense?"
        ],
        "SLEEP": [
            "My baby won’t stop crying—any safe sleeping potion?",
            "I’ve been restless for days—got anything to help me sleep?",
            "The wolves outside won’t leave. Can you help put them to sleep?",
            "I need to sneak by the guards. Can you make them sleep?",
            "The town bard is too lively tonight—anything to quiet the tunes?"
        ],
        "SLOW": [
            "The charging boar won’t stop! Can you slow it down?",
            "My opponent is too quick during our duel—any potions for that?",
            "The river currents are too swift. Can you slow them?",
            "Those thieves always outrun me. Do you have a remedy for that?",
            "I need the workers to slow down—pace themselves. Anything helpful?"
        ],
        "FROST": [
            "The river’s melted, and I need to cross. Got an ice potion?",
            "My drink’s warm! Do you have something to cool it?",
            "The crops are wilting in the heat—can frost cool the field?",
            "We’re chasing a monster. Frost tracks would slow it, right?",
            "I want to make an ice sculpture—anything to help create ice?"
        ],
        "LIGHTNING": [
            "My town’s generator is dead—do you have electric potions?",
            "I need to jolt an old machine back to life. Can you help?",
            "I want to stun a charging bear. Do you have a lightning potion?",
            "I need a dramatic entrance—lightning effects, please!",
            "The storm isn’t striking. Do you have bottled lightning?"
        ],
        "POISON": [
            "There are rats in my basement—got a potion for that?",
            "My rival’s crops are too perfect... any suggestions?",
            "Just give me a poison and don't ask why",
            "I’m hunting venomous creatures. Do you sell poisons?",
            "My traps need better bait. Would a poison work?"
        ],
        "RAGE": [
            "I’m competing in a gladiator match. Can I get a rage boost?",
            "I’m too timid—any potions to help me assert myself?",
            "I need to face off against a bully. What potion could help?",
            "I think i am too kind, is there anything that could help?",
            "My kingdom’s warriors need to fight with fury. Got anything?"
        ]
    }

    customer_pic = [

    ]