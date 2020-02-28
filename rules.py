
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
    {"label": "ON_DRAW_CARD,b", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "second"}, {"LEMMA": "card"}]},
    
    {"label": "DRAW_CARD,A", "pattern": [{"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DRAW_CARD,B", "pattern": [{"LEMMA": "draw"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},

    {"label": "ON_DISCARD_CARD", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,A", "pattern": [{"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,B", "pattern": [{"LEMMA": "discard"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},

    {"label": "ON_DAMAGE", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "deal"}, {"LEMMA": "damage"}]},
    {"label": "ON_ATTACK", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "attack"}]},
    {"label": "ON_ENTER,A", "pattern": [{"LEMMA": "when"}, {"ORTH": "/name/"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_ENTER,B", "pattern": create_pattern("as /name/ enter the battlefield")},
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

    {"label": "ON_CREATURE_ENTER,A", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "another"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_CREATURE_ENTER,B", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "a"}, {"LEMMA": "nontoken"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_CREATURE_ENTER,C", "pattern": [{"LEMMA": "whenever"}, {"LEMMA": "a"}, {"LEMMA": "creature"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},

    {"label": "DAMAGE_OWN,A", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "you"}]},
    {"label": "DAMAGE_CONTROLLER,A", "pattern": [{"ORTH": "/name/"}, {"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "that"}, {"LEMMA": "creature"}, {"LEMMA": "'s"}, {"LEMMA": "controller"} ]},
    {"label": "DAMAGE_PLAYERS", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "each"}, {"LEMMA": "player"}]},
    {"label": "DAMAGE_OPPONENT", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "each"}, {"LEMMA": "opponent"}]},
    {"label": "DAMAGE_ANY", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "any"}, {"LEMMA": "target"}]},
    {"label": "DAMAGE_CREATURE,A", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "target"}, {"LEMMA": "creature"}] },
    {"label": "DAMAGE_CREATURE,B", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "each"}, {"LEMMA": "other"}, {"LEMMA": "creature"}] },
    
    {"label": "ON_LIFE_GAIN,A", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}]},
    {"label": "ON_LIFE_GAIN,B", "pattern": [{"LEMMA": "when"}, {"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}]},

    {"label": "LIFE_GAIN,A", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_GAIN,B", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},
    {"label": "LIFE_GAIN,C", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}, {"LEMMA": "equal"}, {"LEMMA": "to"}]},
    {"label": "LIFE_LOSE_OWN,A", "pattern": [{"LOWER": "you"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OWN,B", "pattern": [{"LOWER": "you"}, {"LEMMA": "lose"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OPPONENT,A", "pattern": [{"LEMMA": "each"}, {"LEMMA": "opponent"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OPPONENT,B", "pattern": [{"LEMMA": "each"}, {"LEMMA": "opponent"}, {"LEMMA": "lose"}, {"LEMMA": "x"}, {"LEMMA": "life"}]},

    {"label": "LIFE_PAY,A", "pattern": create_pattern("pay N life")},

    {"label": "SCRY,A", "pattern": create_pattern("Lscry N")},
    {"label": "SCRY,B", "pattern": create_pattern("( look at the top N card of Lyour library , then put any number of Lthem on the bottom of Lyour library and the rest on top in any order . )")},

    {"label": "DEVOTION_RED", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "red"}]},
    {"label": "DEVOTION_BLACK", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "black"}]},
    {"label": "DEVOTION_BLUE", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "blue"}]},
    {"label": "DEVOTION_WHITE", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "white"}]},
    {"label": "DEVOTION_GREEN", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "green"}]},
    # TODO: devotion to more than one color
    # TODO: remove "devotion" explanation

    {"label": "CREATE_TOKEN,A", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},
    {"label": "CREATE_TOKEN,B", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},

    {"label": "CREATE_FOOD_TOKEN,A", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,B", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LEMMA": "number"}, {"LEMMA": "of"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,C", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LOWER": "food"}, {"LEMMA": "token"}]},

    {"label": "GRAVEYARD_TO_LIBRARY", "pattern": [{"LEMMA": "from"}, {"LOWER": "your"}, {"LEMMA": "graveyard"}, {"LEMMA": "on"}, {"LEMMA": "top"}, {"LEMMA": "of"}, {"LOWER": "your"}, {"LEMMA": "library"},]},
    {"label": "LIBRARY_TO_GRAVEYARD", "pattern": create_pattern("library into Ltheir graveyard")},


    {"label": "RIOT", "pattern": [{"LEMMA": "riot"}]},
    {"label": "FLYING", "pattern": [{"LOWER": "flying"}]},
    {"label": "FLASH", "pattern": [{"LOWER": "flash"}]},
    {"label": "PROLIFERATE", "pattern": [{"LEMMA": "proliferate"}]},
    {"label": "LIFELINK", "pattern": [{"LEMMA": "lifelink"}]},

    {"label": "ENTERS_TAPPED", "pattern": [{"ORTH": "/name/"}, {"LEMMA": "enters"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}, {"LEMMA": "tap"}]},

    {"label": "RETURN_TO_HAND,a", "pattern": create_pattern("return /name/ to Lyour hand")},
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
        PRIMARY KEY(`uuid`)
    ) """)

def insert(conn, uuid, labels):
    conn.execute("""
    INSERT INTO cardlabels (uuid, labels) VALUES (?,?)
    """, [uuid, labels])

def clean_label(label):
    pos = label.find(',')
    if pos > 0:
        return label[0:pos]
    return label

def clean_text(text, name):
    text = text.replace(name, '/name/')
    # Fix names that contain comma and can be reference as both
    # i.e. "Roalesk, Apex Hybrid"
    if name.find(",") > 0:
        shortname = name[0:name.find(",")]
        text = text.replace(shortname, '/name/')
    return text


def run(app, conn):
    import json

    with open("StandardCards.json") as datafile:
        data = json.load(datafile)

    create_table(conn)

    # Disable 'ner' to remove default Named-Entity Recognition
    nlp = spacy.load('en_core_web_sm', disable=['ner'])
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)

    cur = conn.cursor()

    ## TODO: MAKE SQL IN BATCHES
    data_to_save = []

    for cardKey in list(data.keys()):
        card = data[cardKey]
        if 'text' in card:
            name = card['name']

            t = clean_text(card['text'], name)
            doc = nlp(t)

            labels = set([clean_label(ent.label_) for ent in doc.ents])
            labelsStr = ', '.join(str(e) for e in labels)

            insert(cur, card["uuid"], labelsStr)
        else:
            insert(cur, card["uuid"], "")

            #
            # https://docs.python.org/2/library/sqlite3.html#sqlite3-controlling-transactions
            #

            #for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.dep_)
            #print([(ent.text, ent.label_) for ent in doc.ents])

            #displacy.render(doc, style='dep')
            #displacy.render(doc, style='ent')
            

    conn.commit()

def analize(app, conn, uuid):
    import json
    import re

    cur = conn.cursor()
    cur.execute("SELECT * FROM cards WHERE uuid = ?", [uuid])
    cards = cur.fetchall()
    card = cards[0]

    # Disable 'ner' to remove default Named-Entity Recognition
    nlp = spacy.load('en_core_web_sm', disable=['ner'])
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)

    name = card['name']
    t = clean_text(card['text'], name)
    doc = nlp(t)

    # print([(ent.text, ent.label_) for ent in doc.ents])
    totalwords = len(doc)
    labeledwords = 0
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
        if len(token.ent_type_) > 0 or token.pos_ == "PUNCT":
            labeledwords += 1
    lebeledpct = (labeledwords / totalwords) * 100.0

    # print("total "+ str(totalwords) + "  lbl "+ str(labeledwords) + "  pct " + str(lebeledpct))

    labels = set([clean_label(ent.label_) for ent in doc.ents])
    labelsStr = ', '.join(str(e) for e in labels)

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

    mana = []
    if card["manaCost"] is not None:
        manaregex = re.compile(r"{(\w)}", re.IGNORECASE)
        mana = manaregex.findall(card["manaCost"])
    return {
        "card": card,
        "doc": tokens,
        "labels": labelsStr,
        "display_ent": displacy.render(doc, style='ent'),
        "display_dep": displacy.render(doc, style='dep'),
        "mana": mana,
        "totalwords": totalwords,
        "labeledwords": labeledwords,
        "lebeledpct": lebeledpct
    }
