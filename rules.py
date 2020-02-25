
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher

patterns = [
    
    {"label": "ON_DRAW_CARD,1", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "ON_DRAW_CARD,2", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "second"}, {"LEMMA": "card"}]},
    
    {"label": "DRAW_CARD,1", "pattern": [{"LEMMA": "draw"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DRAW_CARD,n", "pattern": [{"LEMMA": "draw"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},

    {"label": "ON_DISCARD_CARD", "pattern": [{"LEMMA": "whenever"}, {"LOWER": "you"}, {"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,1", "pattern": [{"LEMMA": "discard"}, {"LEMMA": "a"}, {"LEMMA": "card"}]},
    {"label": "DISCARD_CARD,2", "pattern": [{"LEMMA": "discard"}, {"LIKE_NUM": True}, {"LEMMA": "card"}]},

    {"label": "ON_DAMAGE", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "deal"}, {"LEMMA": "damage"}]},
    {"label": "ON_ATTACK", "pattern": [{"LEMMA": "whenever"}, {"ORTH": "/name/"}, {"LEMMA": "attack"}]},
    {"label": "ON_ENTER", "pattern": [{"LEMMA": "when"}, {"ORTH": "/name/"}, {"LEMMA": "enter"}, {"LEMMA": "the"}, {"LEMMA": "battlefield"}]},
    {"label": "ON_DIE,1", "pattern": [{"LEMMA": "creature"}, {"LOWER": "you"}, {"LEMMA": "control"}, {"LEMMA": "die"}]},
    {"label": "ON_DIE,2", "pattern": [{"LEMMA": "whenever"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LOWER": "you"}, {"LEMMA": "control"}, {"LEMMA": "die"}]},

    {"label": "DAMAGE_OWN", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "you"}]},
    {"label": "DAMAGE_ALL", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "each"}, {"LEMMA": "player"}]},
    {"label": "DAMAGE_OPPONENT", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LOWER": "each"}, {"LEMMA": "opponent"}]},
    {"label": "DAMAGE_ANY", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "any"}, {"LEMMA": "target"}]},
    {"label": "DAMAGE_CREATURE", "pattern": [{"LEMMA": "deal"}, {"LIKE_NUM": True}, {"LEMMA": "damage"}, {"LEMMA": "to"}, {"LEMMA": "target"}, {"LEMMA": "creature"}], "nums": [1] },
    
    {"label": "ON_LIFE_GAIN", "pattern": [{"LEMMA": "wenever"}, {"LOWER": "you"}, {"LEMMA": "gain"}, {"LEMMA": "life"}]},

    {"label": "LIFE_GAIN", "pattern": [{"LOWER": "you"}, {"LEMMA": "gain"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE", "pattern": [{"LOWER": "you"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},
    {"label": "LIFE_LOSE_OPPONENT", "pattern": [{"LEMMA": "each"}, {"LEMMA": "opponent"}, {"LEMMA": "lose"}, {"LIKE_NUM": True}, {"LEMMA": "life"}]},

    {"label": "SCRY_TOP", "pattern": [{"LEMMA": "look"}, {"LEMMA": "at"}, {"LEMMA": "the"}, {"LEMMA": "top"}, {"LIKE_NUM": True}, {"LEMMA": "card"}, {"LEMMA": "of"}, {"LOWER": "your"}, {"LEMMA": "library"}]},

    {"label": "DEVOTION_RED", "pattern": [{"LOWER": "your"}, {"LEMMA": "devotion"}, {"LEMMA": "to"}, {"LEMMA": "red"}]},

    {"label": "CREATE_TOKEN,1", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},
    {"label": "CREATE_TOKEN,2", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LIKE_NUM": True}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"OP": "?"}, {"LEMMA": "creature"}, {"LEMMA": "token"}]},

    {"label": "CREATE_FOOD_TOKEN,1", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,2", "pattern": [{"LEMMA": "create"}, {"LEMMA": "a"}, {"LEMMA": "number"}, {"LEMMA": "of"}, {"LOWER": "food"}, {"LEMMA": "token"}]},
    {"label": "CREATE_FOOD_TOKEN,3", "pattern": [{"LEMMA": "create"}, {"LIKE_NUM": True}, {"LOWER": "food"}, {"LEMMA": "token"}]},

    {"label": "GRAVEYARD_TO_LIBRARY", "pattern": [{"LEMMA": "from"}, {"LOWER": "your"}, {"LEMMA": "graveyard"}, {"LEMMA": "on"}, {"LEMMA": "top"}, {"LEMMA": "of"}, {"LOWER": "your"}, {"LEMMA": "library"},]},
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

def run(conn):
    import json

    with open("StandardCards.json") as datafile:
        data = json.load(datafile)

    create_table(conn)

    # Disable 'ner' to remove default Named-Entity Recognition
    nlp = spacy.load('en_core_web_sm', disable=['ner'])
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(patterns)

    nlp.add_pipe(ruler)

    output_data = []

    cur = conn.cursor()

    for cardKey in list(data.keys()):
        card = data[cardKey]
        if 'text' in card:
            name = card['name']
            t = card['text']
            t = t.replace(name, '/name/')
            doc = nlp(t)

            #print("----------------------------")
            labels = set([clean_label(ent.label_) for ent in doc.ents])
            labelsStr = ', '.join(str(e) for e in labels)
            #print("*** " + card["name"] + " *** " + labelsStr)
            #print("text:", t)

            output_data.append({"uuid": card["uuid"], "labels": labelsStr})
            insert(cur, card["uuid"], labelsStr)

            """ Find numbers
            for ent in doc.ents:
                label = ent.label_
                #print("- [", label,"]" , ent.text, ent.start, ent.end)
                #print(doc[ent.start:ent.end])
                pattern = get_pattern(label)
                #print("- pattern:", pattern)
                for n in get_num_tokens(pattern):
                    numText = doc[ent.start+n].text
                    num = to_integer(numText)
                    print("- num", numText, "->", num)
            """
            

            #for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.dep_)

            #displacy.render(doc, style='dep')
            #displacy.render(doc, style='ent')
            
            #print([(ent.text, ent.label_) for ent in doc.ents])

            #print(doc.to_json())
            #for token in doc:
            #    print(token.text, token.lemma_, token.pos_, token.dep_)

    conn.commit()
    conn.close()

    with open('card_labels.json', 'w') as f:
        json.dump(output_data, f)

def analize(app, conn, uuid):
    import json

    cur = conn.cursor()
    cur.execute("SELECT * FROM cards WHERE uuid = ?", [uuid])
    cards = cur.fetchall()

    # Disable 'ner' to remove default Named-Entity Recognition
    nlp = spacy.load('en_core_web_sm', disable=['ner'])
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)

    results = []
    for card in cards:
        name = card['name']
        t = card['text']
        t = t.replace(name, '/name/')
        doc = nlp(t)

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
                "ent_type": clean_label(token.ent_type_),

            }
            tokens.append(token)

        results.append({
            "card": card,
            "doc": tokens
        })

    return results