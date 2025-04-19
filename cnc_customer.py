import random

import pygame as pg
from cnc_config import Config
from cnc_potion import Potion
from cnc_inventory import Inventory

customer_rq = {
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

