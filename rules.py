import re

import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher

def create_pattern(str):
    pattern = []
    for w in str.split(" "):
        if w.startswith("L"):
            pattern.append({"LOWER": w[1:]})
        elif w == '/name/':
            pattern.append({"ORTH": w})
        elif w == 'N':
            pattern.append({"LIKE_NUM": True})
        elif w == '?':
            pattern.append({"OP": "?"})
        else:
            pattern.append({"LEMMA": w})

    return pattern

patterns = [
    
    {"label": "ON_DRAW_CARD,A", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "ON_DRAW_CARD,B", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "second"}, {"LEMMA": "card"}]},
    {"label": "ON_DRAW_CARD,C", "pattern": create_pattern("whenever Lyou draw Lyour second card each turn")},
    
    {"label": "DRAW_CARD,A", "pattern": [{"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DRAW_CARD,B", "pattern": [{"LEMMA": "draw"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},
    {"label": "DRAW_CARD,C", "pattern": create_pattern("each player draw Lx card")},

    {"label": "ON_DISCARD_CARD", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,A", "pattern": [{"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,B", "pattern": [{"LEMMA": "discard"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,C", "pattern": create_pattern("discard all the card in Ltheir hand")},
    {"label": "DISCARD_CARD,D", "pattern": create_pattern("discard Lyour hand")},
    {"label": "DISCARD_CARD,E", "pattern": create_pattern("that player discard that card")},

    {"label": "ON_DAMAGE", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "deal"}, {"LEMMA": "damage"}]},
    {"label": "ON_ATTACK,A", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "attack"}]},
    {"label": "ON_ATTACK,B", "pattern": create_pattern("whenever a ? token Lyou control with power N or great attack")},

    {"label": "ON_ENTER,A", "pattern": [{"LEMMA": "when"}, {"ORTH": "/name/"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_ENTER,B", "pattern": create_pattern("as /name/ enter the battlefield")},
    {"label": "ON_ENTER,C", "pattern": create_pattern("each other ? ? ? creature Lyou control enter the battlefield")},

    {"label": "ON_DIE,A", "pattern": [{"LEMMA": "creature"}, {"LOWER": "you"}, {"LEMMA": "control"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,B", "pattern": [{"LEMMA": "whenever"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LOWER": "you"}, {"LEMMA": "control"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,C", "pattern": [{"LEMMA": "when"}, {"ORTH": "/name/"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,D", "pattern": [{"LEMMA": "when"}, {"LEMMA": "enchant"}, {"LEMMA": "creature"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,E", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "an"}, {"LEMMA": "enchant"}, {"LEMMA": "creature"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,F", "pattern": [{"LEMMA": "when"}, {"LEMMA": "this"}, {"LEMMA": "creature"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,G", "pattern": [{"LEMMA": "when"}, {"LEMMA": "this"}, {"LEMMA": "creature"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,H", "pattern": create_pattern("whenever a creature with a coin counter on Lit die")},
    {"label": "ON_DIE,I", "pattern": create_pattern("whenever /name/ or another creature or planeswalker Lyou control die")},
    {"label": "ON_DIE,J", "pattern": create_pattern("whenever another creature die")},
    {"label": "ON_DIE,K", "pattern": create_pattern("whenever an ? Lyou control die")},
    # TODO: "Daxos, Blessed by the Sun": Whenever another creature you control enters the battlefield or dies
    # TODO: "Pelt Collector": Whenever another creature you control enters the battlefield or dies

    {"label": "ON_END_STEP,A", "pattern": create_pattern("at the beginning of Lyour end step")},
    {"label": "ON_END_STEP,B", "pattern": create_pattern("at the beginning of the end step")},
    {"label": "ON_UPKEEP_STEP,A", "pattern": create_pattern("at the beginning of Lyour upkeep")},
    {"label": "ON_COMBAT_STEP,A", "pattern": create_pattern("at the beginning of combat on Lyour turn")},

    {"label": "ON_CREATURE_ENTER,A", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "another"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_CREATURE_ENTER,B", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "a"}, {"LEMMA": "nontoken"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_CREATURE_ENTER,C", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "a"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},

    {"label": "ON_CREATE_CREATURE_TOKEN,A", "pattern": create_pattern("if one or more creature token would be create under Lyour control")},

    {"label": "ON_TAP,A", "pattern": create_pattern("whenever /name/ become tapped")},
    {"label": "TAP_CREATURE,A", "pattern": create_pattern("tap target creature an opponent control")},
    {"label": "TAP_CREATURE,B", "pattern": create_pattern("tap another target creature")},
    {"label": "TAP_CREATURE,C", "pattern": create_pattern("tap up to N target creature")},
    

    {"label": "DAMAGE_OWN,A", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "you"}]},
    {"label": "DAMAGE_CONTROLLER,A", "pattern": [{"ORTH": "/name/"}, {"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "that"}, {"LEMMA": "creature"}, {"LEMMA": "'s"}, {"LEMMA": "controller"} ]},
    {"label": "DAMAGE_PLAYERS", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "each"}, {"LEMMA": "player"}]},
    {"label": "DAMAGE_OPPONENT", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "each"}, {"LEMMA": "opponent"}]},
    {"label": "DAMAGE_ANY,A", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "any"}, {"LEMMA": "target"}]},
    {"label": "DAMAGE_ANY,B", "pattern": create_pattern("/name/ deal N damage to any target")},
    {"label": "DAMAGE_CREATURE,A", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "target"}, {"LEMMA": "creature"}] },
    {"label": "DAMAGE_CREATURE,B", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "each"}, {"LEMMA": "other"}, {"LEMMA": "creature"}] },
    {"label": "DAMAGE_CREATURE,C", "pattern": create_pattern("/name/ deal ? ? damage to target creature") },
    {"label": "DAMAGE_CREATURE,D", "pattern": create_pattern("deal damage equal to Lits power to target creature") },

    {"label": "ON_LIFE_GAIN,A", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}]},
    {"label": "ON_LIFE_GAIN,B", "pattern": [{"LEMMA": "when"}, {"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}]},

    {"label": "LIFE_GAIN,A", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_GAIN,B", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},
    {"label": "LIFE_GAIN,C", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}, {"LEMMA": "equal"}, {"LEMMA": "to"}]},
    {"label": "LIFE_LOSE_OWN,A", "pattern": [{"LOWER": "you"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OWN,B", "pattern": [{"LOWER": "you"}, {"LEMMA": "lose"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OPPONENT,A", "pattern": [{"LEMMA": "each"}, {"LEMMA": "opponent"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OPPONENT,B", "pattern": [{"LEMMA": "each"}, {"LEMMA": "opponent"}, {"LEMMA": "lose"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_TARGET_PLAYER,A", "pattern": create_pattern("any number of target player each lose N life")},

    {"label": "LIFE_PAY,A", "pattern": create_pattern("pay N life")},

    {"label": "SCRY,A", "pattern": create_pattern("Lscry N")},
    {"label": "SCRY,B", "pattern": create_pattern("( look at the top N card of Lyour library , then put any number of Lthem on the bottom of Lyour library and the rest on top in any order . )")},
    {"label": "SCRY,C", "pattern": create_pattern("( look at the top card of Lyour library . Lyou may put that card on the bottom of Lyour library . )")},

    {"label": "DEVOTION_RED", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "red"}]},
    {"label": "DEVOTION_BLACK", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "black"}]},
    {"label": "DEVOTION_BLUE", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "blue"}]},
    {"label": "DEVOTION_WHITE", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "white"}]},
    {"label": "DEVOTION_GREEN", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "green"}]},
    # TODO: devotion to more than one color
    # TODO: remove "devotion" explanation:  (Each {W} in the mana costs of permanents you control counts towards your devotion to white DEVOTION_WHITE .)

    {"label": "AMASS,A", "pattern": create_pattern("Lamass N")},
    {"label": "AMASS,B", "pattern": create_pattern("Lamass Lx")},
    # TODO: capture amass description

    {"label": "AFTERLIFE,A", "pattern": create_pattern("Lafterlife N")},

    {"label": "CREATE_CREATURE_TOKEN,A", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},
    {"label": "CREATE_CREATURE_TOKEN,B", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},
    {"label": "CREATE_CREATURE_TOKEN,C", "pattern": create_pattern("create a number of N ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,D", "pattern": create_pattern("create that many N ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,E", "pattern": create_pattern("create Lx N ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,F", "pattern": create_pattern("that many N ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,G", "pattern": create_pattern("create an ? ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,H", "pattern": create_pattern("create a N ? ? ? ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,I", "pattern": create_pattern("create N N ? ? ? ? ? creature token")},
    {"label": "CREATE_CREATURE_TOKEN,J", "pattern": create_pattern("create a ? ? ? creature token with")},


    {"label": "CREATE_FOOD_TOKEN,A", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,B", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LEMMA": "number"}, {"LEMMA": "of"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,C", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,D", "pattern": create_pattern("( a Lfood token be an artifact with \" { 2 } , { T } , Sacrifice this artifact : Lyou gain 3 life . \" )")},
    {"label": "CREATE_FOOD_TOKEN,E", "pattern": create_pattern("( Lit be an artifact with \" { 2 } , { T } , Sacrifice this artifact : Lyou gain 3 life . \" )")},
    {"label": "ON_SACRIFICE_FOOD_TOKEN,A", "pattern": create_pattern("whenever Lyou sacrifice a food")},

    {"label": "GRAVEYARD_TO_LIBRARY", "pattern": [{"LEMMA": "from"}, {"LOWER": "your"}, {"LEMMA": "graveyard"}, {"LEMMA": "on"}, {"LEMMA": "top"}, {"LEMMA": "of"}, {"LOWER": "your"}, {"LEMMA": "library"},]},
    {"label": "LIBRARY_TO_GRAVEYARD,A", "pattern": create_pattern("library into Ltheir graveyard")},
    {"label": "LIBRARY_TO_GRAVEYARD,B", "pattern": create_pattern("put the top N card of Lyour library into Lyour graveyard")},
    {"label": "LIBRARY_TO_EXILE,A", "pattern": create_pattern("exile the top card of Lyour library")},
    {"label": "LIBRARY_TO_EXILE,B", "pattern": create_pattern("exile the top N card of Lyour library")},
    {"label": "GRAVEYARD_TO_HAND,A", "pattern": create_pattern("return /name/ from Lyour graveyard to Lyour hand")},

    {"label": "EXILE_TO_GRAVEYARD,A", "pattern": create_pattern("from exile into that player 's graveyard")},
  
    {"label": "EXILE,A", "pattern": create_pattern("exile that card from Lyour graveyard")},
    {"label": "EXILE,B", "pattern": create_pattern("exile that card")},
    {"label": "EXILE,C", "pattern": create_pattern("( then exile this card . Lyou may cast the creature later from exile . )")},
    {"label": "EXILE,C2", "pattern": create_pattern("( then exile this spell . Lyou may cast the creature later from exile . )")},
    {"label": "EXILE,D", "pattern": create_pattern("then that player exile a card from Ltheir hand")},
    {"label": "EXILE,E", "pattern": create_pattern("Lexile /name/")},
    {"label": "EXILE,F", "pattern": create_pattern("Lexile /name/ from Lyour graveyard")},
    {"label": "EXILE,G", "pattern": create_pattern("Lexile target card from a graveyard")},
    {"label": "EXILE,H", "pattern": create_pattern("Lexile target ? an opponent control")},
    {"label": "EXILE,I", "pattern": create_pattern("Lexile target opponent 's graveyard")},
    {"label": "EXILE,J", "pattern": create_pattern("Lexile up to ? ? target card from graveyard")},
    {"label": "EXILE,K", "pattern": create_pattern("Lexile target card from an opponent 's graveyard")},
    {"label": "EXILE,L", "pattern": create_pattern("exile target creature with")},
    {"label": "EXILE,M", "pattern": create_pattern("exile target creature that player control")},
    {"label": "EXILE,M1", "pattern": create_pattern("exile target permanent Lyou control")},
    {"label": "EXILE,M2", "pattern": create_pattern("exile up to N other target creature Lyou control")},
    {"label": "EXILE,N", "pattern": create_pattern("exile target permanent with")},    
    {"label": "EXILE,O", "pattern": create_pattern("exile target creature or planeswalker")},    
    {"label": "EXILE,P", "pattern": create_pattern("an opponent exile a nonland card from among Lthem")},
    {"label": "EXILE,Q", "pattern": create_pattern("Lyou may exile ? ? card from ? graveyard")},
    {"label": "EXILE,R", "pattern": create_pattern("exile each opponent 's graveyard")},
    {"label": "EXILE,S", "pattern": create_pattern("each opponent exile the top N card of Ltheir library")},
    {"label": "EXILE,T", "pattern": create_pattern("exile target creature")},
    {"label": "EXILE,U", "pattern": create_pattern("exile target creature or enchantment")},
    {"label": "EXILE,V", "pattern": create_pattern("exile target artifact")},
    {"label": "EXILE,W", "pattern": create_pattern("exile target enchantment")},
    {"label": "EXILE,X", "pattern": create_pattern("exile target nonland permanent")},
    {"label": "EXILE,Y", "pattern": create_pattern("exile enchant creature")},
    {"label": "EXILE,Z", "pattern": create_pattern("Lyou may exile Lit")},
    {"label": "EXILE,AA", "pattern": create_pattern("exile Lit instead")},
    {"label": "EXILE,AB", "pattern": create_pattern("exile another target creature Lyou own")},
    {"label": "EXILE,AC", "pattern": create_pattern("exile a creature card from Lyour graveyard")},
    {"label": "EXILE,AD", "pattern": create_pattern("exile target nonland permanent an opponent control")},
    {"label": "EXILE,AE", "pattern": create_pattern("exile all creature card in all graveyard")},
    {"label": "EXILE,AF", "pattern": create_pattern("exile that creature until /name/ leave the battlefield")},
    {"label": "EXILE,AG", "pattern": create_pattern("Lexile N ? card from Lyour graveyard")},
    {"label": "EXILE,AH", "pattern": create_pattern("Lexile N target card from an opponent 's graveyard")},
    {"label": "EXILE,AI", "pattern": create_pattern("exile all Lmulticolored permanent")},
    {"label": "EXILE,AJ", "pattern": create_pattern("exile the top card of Ltheir library")},
    {"label": "EXILE,AK", "pattern": create_pattern("target player exile a card from Ltheir graveyard")},
    {"label": "EXILE,AK", "pattern": create_pattern("exile those ? at the beginning of Lyour next end step")},
    # Continue on T


    {"label": "RETURN_TO_HAND,A", "pattern": create_pattern("return /name/ to Lyour hand")},
    {"label": "RETURN_TO_HAND,B", "pattern": create_pattern("Lreturn target nonland permanent to Lits owner 's hand")},
    {"label": "RETURN_TO_HAND,C", "pattern": create_pattern("return /name/ to Lits owner 's hand")},
    {"label": "RETURN_TO_HAND,D", "pattern": create_pattern("return target creature to Lits owner 's hand")},

    {"label": "RIOT,A", "pattern": create_pattern("riot")},
    {"label": "RIOT,B", "pattern": create_pattern("( this creature enter the battlefield with Lyour choice of a +1/+1 counter or haste . )")},
    {"label": "RIOT,C", "pattern": create_pattern("( Lthey enter the battlefield with Lyour choice of a +1/+1 counter or haste . )")},

    {"label": "FLYING,A", "pattern": create_pattern("Lflying ( this creature can not be block except by creature with fly or reach . )")},
    {"label": "FLYING,Z", "pattern": [{"LOWER": "flying"}]},

    {"label": "FLASH", "pattern": [{"LOWER": "flash"}]},
    {"label": "TRAMPLE", "pattern": [{"LOWER": "trample"}]},
    
    {"label": "HASTE,A", "pattern": create_pattern("Lhaste ( this creature can attack and { t } as soon as Lit come under Lyour control . )")},
    {"label": "HASTE,Z", "pattern": [{"LOWER": "haste"}]},
    
    {"label": "PROLIFERATE,A", "pattern": [{"LEMMA": "proliferate"}]},
    {"label": "PROLIFERATE,B", "pattern": create_pattern("( choose any number of permanent and/or player , then give each another counter of each kind already there . )")},

    {"label": "LIFELINK", "pattern": [{"LEMMA": "lifelink"}]},
    {"label": "DEATHTOUCH", "pattern": [{"LEMMA": "deathtouch"}]},
    {"label": "VIGILANCE", "pattern": [{"LEMMA": "vigilance"}]},
    
    {"label": "REACH,A", "pattern": [{"LEMMA": "reach"}]},
    {"label": "REACH,B", "pattern": create_pattern("( this creature can block creature with fly . )")},
    
    
    {"label": "INDESTRUCTIBLE", "pattern": create_pattern("Lindestructible")},
    {"label": "DEFENDER", "pattern": create_pattern("Ldefender")},
    {"label": "FIRST_STRIKE", "pattern": create_pattern("first strike")},
    {"label": "DOUBLE_STRIKE", "pattern": create_pattern("double strike")},
    {"label": "ENTERS_TAPPED", "pattern": [{"ORTH": "/name/"}, {"LEMMA": "enters"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}, {"LEMMA": "tap"}]},
    {"label": "MENACE", "pattern": create_pattern("Lmenace ( this creature can not be block except by two or more creature . )")},

    {"label": "SURVEIL,A", "pattern": create_pattern("Lsurveil N . ( look at the top two card of Lyour library , then put any number of Lthem into Lyour graveyard and the rest on top of Lyour library in any order . )")},
    {"label": "SURVEIL,B", "pattern": create_pattern("Lsurveil 1 . ( look at the top card of Lyour library . Lyou may put that card into Lyour graveyard . )")},
    {"label": "SURVEIL,C", "pattern": create_pattern("( to surveil N , look at the top N card of Lyour library , then put any number of Lthem into Lyour graveyard and the rest on top of Lyour library in any order . )")},
    {"label": "SURVEIL,D", "pattern": create_pattern("Lsurveil 1 . ( look at the top card of Lyour library . Lyou may put Lit into Lyour graveyard . )")},
    {"label": "SURVEIL,F", "pattern": create_pattern("Lsurveil N . ( look at the top N card of Lyour library , then put any number of Lthem into Lyour graveyard and the rest on the top of Lyour library in any order . )")},
    {"label": "SURVEIL,G", "pattern": create_pattern("Lsurveil N")},
    {"label": "ON_SURVEIL,A", "pattern": create_pattern("each time Lyou surveil")},
    {"label": "ON_SURVEIL,B", "pattern": create_pattern("whenever Lyou surveil")},
    {"label": "ON_SURVEIL,C", "pattern": create_pattern("as long as Lyou have Lsurveilled this turn")},

    {"label": "HEXPROOF,A", "pattern": create_pattern("hexproof")},
    {"label": "HEXPROOF,B", "pattern": create_pattern("can not be the target of spell or Labilities Lyour opponent control . )")},

    {"label": "CONVOKE,A", "pattern": create_pattern("Lconvoke")},
    {"label": "CONVOKE,B", "pattern": create_pattern("( Lyour creature can help cast this spell . each creature Lyou tap while cast this spell pay for { 1 } or one mana of that creature 's color . )")},
    # TODO: capture convoke explanation

    {"label": "MANA_COST_REDUCED,A", "pattern": create_pattern("without pay Ltheir mana cost")},
    {"label": "MANA_COST_REDUCED,B", "pattern": create_pattern("this spell cost { N } less to cast")},
    {"label": "MANA_COST_REDUCED,C", "pattern": create_pattern("enchantment spell Lyou cast cost { N } less to cast")},
    {"label": "MANA_COST_REDUCED,D", "pattern": create_pattern("spell Lyou cast cost { N } less to cast")},
    {"label": "MANA_COST_REDUCED,E", "pattern": create_pattern("spell Lyou cast with convert mana cost N or ? cost { N } less to cast")},
    {"label": "MANA_COST_REDUCED,F", "pattern": create_pattern("Lthey cost { N } less to cast")},
    {"label": "MANA_COST_REDUCED,G", "pattern": create_pattern("this spell cost { X } less to cast")},
    {"label": "MANA_COST_REDUCED,H", "pattern": create_pattern("without pay Lits mana cost")},
    {"label": "MANA_COST_REDUCED,I", "pattern": create_pattern("cost { N } less to activate")},
    # TODO: Return those cards to the battlefield? would be reduced mana cost ?

    {"label": "MANA_COST_INCREASED,A", "pattern": create_pattern("Lspells Lyour opponent cast that target /name/ cost { N } more to cast")},
    {"label": "MANA_COST_INCREASED,B", "pattern": create_pattern("Lyour opponent control cost { N } more to activate")},
    {"label": "MANA_COST_INCREASED,C", "pattern": create_pattern("Lyour opponent activate cost { N } more to activate")},

    {"label": "SPECTACLE,A", "pattern": create_pattern("Lspectacle { ? } ( Lyou may cast this spell for Lits spectacle cost rather than Lits mana cost if an opponent lose life this turn . )")},
    {"label": "SPECTACLE,B", "pattern": create_pattern("Lspectacle { ? }")},
    # TODO: spectable is MANA_COST_REDUCED too !

    {"label": "SAGA", "pattern": create_pattern("as this Lsaga enter and after Lyour draw step , add a lore counter . sacrifice after")},

    {"label": "GAIN_CONTROL_CREATURE", "pattern": create_pattern("gain control of target creature")},

    {"label": "CREATURE_BONUS_END_TURN,A", "pattern": create_pattern("other ? Lyou control get ? until end of turn")},
    {"label": "CREATURE_BONUS_END_TURN,B", "pattern": create_pattern("target creature Lyou control get ? until end of turn")},
    {"label": "CREATURE_BONUS_END_TURN,C", "pattern": create_pattern("creature Lyou control get ? until end of turn")},
    {"label": "CREATURE_BONUS_END_TURN,E", "pattern": create_pattern("creature Lyou control each get ? until end of turn")},
    {"label": "CREATURE_BONUS_END_TURN,F", "pattern": create_pattern("until end of turn , creature Lyou control get ?")},
    {"label": "CREATURE_BONUS_END_TURN,G", "pattern": create_pattern("/name/ get ? until end of turn")},

    {"label": "CREATURE_BONUS,A", "pattern": create_pattern("other ? Lyou control get ?")},
    {"label": "CREATURE_BONUS,B", "pattern": create_pattern("creature Lyou control get ?")},
    {"label": "CREATURE_BONUS,C", "pattern": create_pattern("Lcreatures Lyou control get ?")},
    {"label": "CREATURE_BONUS,D", "pattern": create_pattern("another target ? Lyou control get ?")},
    {"label": "CREATURE_BONUS,E", "pattern": create_pattern("/name/ get ? for each")},
    # TODO: Tower Defense: check get +1/+1 and gains ...
    # TODO: Gruul Beastmaster: check +X/+0
    # TODO: Burning-Yard Trainer: +2+/2 and gains haste until...
    # TODO: Gift of the Fae: ... and gain
    #{"label": "CREATURE_BONUS,F", "pattern": create_pattern("target creature get ?")},

    {"label": "CREATURE_MALUS_END_TURN,A", "pattern": create_pattern("target creature get ? until end of turn")},
    {"label": "CREATURE_MALUS_END_TURN,B", "pattern": create_pattern("all creature get ? until end of turn")},

    {"label": "CREATURE_MALUS,A", "pattern": create_pattern("creature Lyour opponent control get ?")},

    {"label": "DESTROY_CREATURE,A", "pattern": create_pattern("destroy target creature")},
    {"label": "DESTROY_ARTIFACT,A", "pattern": create_pattern("destroy target artifact")},

    {"label": "ANY_NUMBER_OF_CARDS,A", "pattern": create_pattern("a deck can have any number of card name ?")},
    {"label": "ANY_NUMBER_OF_CARDS,B", "pattern": create_pattern("a deck can have up to N card name ?")},

    {"label": "ESCAPE,A", "pattern": create_pattern("Lescape - ? ? ? ? , Lexile N other card from Lyour graveyard . ( Lyou may cast this card from Lyour graveyard for Lits escape cost . )")},
    {"label": "ESCAPE,B", "pattern": create_pattern("( Lyou may cast ? ? from Lyour graveyard for ? escape cost . )")},
    {"label": "ESCAPE,C", "pattern": create_pattern("Lescape - ? ? ? ? ? , Lexile N other card from Lyour graveyard")},

    {"label": "SACRIFICE_AS_COST,A", "pattern": create_pattern("as an additional cost to cast this spell , sacrifice a creature .")},
    {"label": "SACRIFICE_AS_COST,B", "pattern": create_pattern("Lsacrifice N other creature")},

    {"label": "SACRIFICE_CREATURE,A", "pattern": create_pattern("sacrifice a creature")},

    {"label": "ON_SACRIFICE_PERMANENT,A", "pattern": create_pattern("whenever Lyou sacrifice another permanent")},

    {"label": "COUNTER_PUT,A", "pattern": create_pattern("put ? +1/+1 counter on each creature Lyou control")},
    {"label": "COUNTER_PUT,B1", "pattern": create_pattern("put ? +1/+1 counter on target ? Lyou control")},
    {"label": "COUNTER_PUT,B2", "pattern": create_pattern("put ? +1/+1 counter on target creature")},
    {"label": "COUNTER_PUT,B3", "pattern": create_pattern("put a +1/+1 counter on up to N target creature Lyou control")},
    {"label": "COUNTER_PUT,B4", "pattern": create_pattern("put a +1/+1 counter on each of those creature")},
    {"label": "COUNTER_PUT,C1", "pattern": create_pattern("put ? +1/+1 counter on each of up to N target creature")},
    {"label": "COUNTER_PUT,C2", "pattern": create_pattern("put N +1/+1 counter on up to one target creature")},
    {"label": "COUNTER_PUT,D1", "pattern": create_pattern("/name/ enter the battlefield with ? +1/+1 counter on Lit")},
    {"label": "COUNTER_PUT,D2", "pattern": create_pattern("/name/ enter the battlefield with a number of +1/+1 counter on Lit")},
    {"label": "COUNTER_PUT,D3", "pattern": create_pattern("enter the battlefield with an additional +1/+1 counter on Lit")},
    {"label": "COUNTER_PUT,D4", "pattern": create_pattern("enter with an additional +1/+1 counter on Lit")},
    {"label": "COUNTER_PUT,E", "pattern": create_pattern("put ? +1/+1 counter on Lit")},
    {"label": "COUNTER_PUT,F", "pattern": create_pattern("put ? +1/+1 counter on /name/")},
    {"label": "COUNTER_PUT,H", "pattern": create_pattern("put that many +1/+1 counter on /name/")},
    {"label": "COUNTER_PUT,I", "pattern": create_pattern("distribute ? +1/+1 counter among ? ? ? ? ? ? target creature")},
    {"label": "COUNTER_PUT,J", "pattern": create_pattern("double the number of +1/+1 counter on each of those creature")},
    {"label": "COUNTER_PUT,K1", "pattern": create_pattern("put ? +1/+1 counter on target land Lyou control")},
    {"label": "COUNTER_PUT,K2", "pattern": create_pattern("put ? +1/+1 counter on up to one target noncreature land Lyou control")},
    {"label": "COUNTER_PUT,L", "pattern": create_pattern("move ? +1/+1 counter from /name/ onto target creature")},
     

    {"label": "COUNTER_REMOVE,A", "pattern": create_pattern("remove that many +1/+1 counter from /name/")},

]


def get_labels():
    labels = set()
    for pattern in patterns:
        cl = clean_label(pattern["label"])
        labels.add(cl)
    return labels

def get_trigger_labels():
    triggers = set()
    for label in get_labels():
        if label.startswith('ON_'):
            triggers.add(label)
    return triggers

def get_effect_labels():
    effects = set()
    for label in get_labels():
        if not label.startswith('ON_'):
            effects.add(label)
    return effects

def get_pattern(label):
    for pattern in patterns:
        if pattern["label"] == label:
            return pattern
    return None

def get_num_tokens(pattern):
    nums = []
    for counter, token in enumerate(pattern["pattern"]):
        if "LIKE_NUM" in token and token["LIKE_NUM"]:
            nums.append(counter)
    return nums

def to_integer(t):
    try:
        return int(t)
    except:
        if t == 'a' or t == 'one':
            return 1
        if t == 'two':
            return 2
        if t == 'three':
            return 3
        if t == 'four':
            return 4
        if t == 'five':
            return 5
        if t == 'six':
            return 6
        if t == 'seven':
            return 7
        if t == 'eight':
            return 8
        if t == 'nine':
            return 9
        if t == 'ten':
            return 10
        
        return t

def create_table(conn):
    conn.execute("""DROP TABLE IF EXISTS cardlabels""")
    conn.execute("""CREATE TABLE cardlabels (
        uuid TEXT,
        labels TEXT,
        all_labels TEXT,
        mana TEXT,
        totalwords INTEGER,
        labeledwords INTEGER,
        labeledpct REAL,
        PRIMARY KEY(`uuid`)
    ) """)

def insert(conn, uuid, analysis):
    conn.execute("""
    INSERT INTO cardlabels (uuid, labels, all_labels, mana, totalwords, labeledwords, labeledpct)
    VALUES (?,?,?,?,?,?,?)
    """, [uuid, analysis["labels"], analysis["all_labels"], analysis["mana"], analysis["totalwords"], analysis["labeledwords"], analysis["labeledpct"] ])

def clean_label(label):
    pos = label.find(',')
    if pos > 0:
        return label[0:pos]
    return label

def clean_text(text, name):
    if text is not None:
        text = text.replace(name, '/name/')
        # Fix names that contain comma and can be reference as both
        # i.e. "Roalesk, Apex Hybrid"
        if name.find(",") > 0:
            shortname = name[0:name.find(",")]
            text = text.replace(shortname, '/name/')

        # Fix name at the end of phrase
        text = text.replace("/name/.", "/name/ .")

        # Remove dash
        text = text.replace('—', ' - ')

    return text


def run(app, conn):
    import json

    with open("StandardCards.json") as datafile:
        data = json.load(datafile)

    create_table(conn)

    nlp = create_nlp()

    ## TODO: MAKE SQL IN BATCHES
    data_to_save = []

    cur = conn.cursor()

    for cardKey in list(data.keys()):
        card = data[cardKey]
        if 'text' in card:
            analysis = get_card_analysis(nlp, card, False)
            insert(cur, card["uuid"], analysis)
        else:
            insert(cur, card["uuid"], analysis)

    conn.commit()

def analize(app, conn, name):
    import json

    cur = conn.cursor()
    cur.execute("SELECT * FROM cards WHERE name = ?", [name])
    cards = cur.fetchall()
    card = cards[0]

    return get_card_analysis(create_nlp(), card, True)

def create_nlp():
    # Disable 'ner' to remove default Named-Entity Recognition
    nlp = spacy.load('en_core_web_sm', disable=['ner'])
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)

    return nlp    

def get_card_analysis(nlp, card, forDisplay):
    name = card['name']
    t = ""
    if card['text'] is not None:
        t = clean_text(card['text'], name)

    doc = nlp(t)

    # print([(ent.text, ent.label_) for ent in doc.ents])
    totalwords = len(doc)
    labeledwords = 0
    labeledpct = 0.0
    for token in doc:
        #print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
        if len(token.ent_type_) > 0 or token.pos_ == "PUNCT" or token.pos_ == "SPACE":
            labeledwords += 1
    if totalwords > 0:
        labeledpct = (labeledwords / totalwords) * 100.0

    labels = set([clean_label(ent.label_) for ent in doc.ents])
    labelsStr = ', '.join(str(e) for e in labels)
    all_labels = ','.join(set([ent.label_ for ent in doc.ents]))

    tokens = []
    for token in doc:
        # app.logger.info("token: [%s]", token)
        # https://spacy.io/api/token#attributes
        token = {
            "text": token.text,
            "lemma": token.lemma_,
            "norm": token.norm_,
            "lower": token.lower_,
            "like_num": token.like_num,
            "pos": token.pos_,
            "dep": token.dep_,
            "ent_type": clean_label(token.ent_type_)
        }
        tokens.append(token)

    manaStr = ""
    try:
        manaregex = re.compile(r"{(\w|\w\/\w)}", re.IGNORECASE)
        mana = manaregex.findall(card["manaCost"])
        manaStr = ','.join(m.replace("/", "") for m in mana)
    except:
        pass

    display_ent = None
    display_dep = None
    if forDisplay:
        display_ent = displacy.render(doc, style='ent')
        display_dep = displacy.render(doc, style='dep')

    # TODO: use epoch time for the moment.
    import time
    updated_on = int(time.time())
    
    return {
        "card": card,
        "doc": tokens,
        "labels": labelsStr,
        "all_labels": all_labels,
        "display_ent": display_ent,
        "display_dep": display_dep,
        "mana": manaStr,
        "totalwords": totalwords,
        "labeledwords": labeledwords,
        "labeledpct": labeledpct,
        "updated_on": updated_on
    }
