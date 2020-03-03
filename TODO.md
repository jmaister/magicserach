

# All card details


    <!--
    <h2>Debug</h2>
    <table>
    {% for k in analysis.card.keys() %}
        <tr>
            <td>{{k}}</td>
            <td>{{analysis.card[k]}}</td>
        </tr>
    {% endfor %}
    </table>

    <p>{{analysis}}</p>
    -->

# Card images

Get from here: https://scryfall.com/docs/api/images


# Doc analysis

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.dep_)
    
    print([(ent.text, ent.label_) for ent in doc.ents])

    displacy.render(doc, style='dep')
    displacy.render(doc, style='ent')


# Special cards

Foulmire Knight

Invert

Revival / Revenge
convertedManaCost 	8.0 ?

# Stats queries

## Action stats

select count(*), type from history
group by type


# TODO:

## Jump start (10)

 Jump-start (You may cast this card from your graveyard by discarding a card in addition to paying its other costs. Then exile this card.)

## Create copy (24)

Quasiduplicate
Create a token that's a copy of target creature you control.


## Counters (85)

+1/+1 counter
with an additional +1/+1 counter on it
/name/ escapes with a +1/+1 counter on it.
Woe Strider escapes with two +1/+1 counters on it.

Polukranos, Unchained
/name/ enters the battlefield with six +1/+1 counters on it

## Adamant (17)

Adamant - if at least...

## Sacrifice (168)

sacrifice /name/

## Fight (20)

Polukranos, Unchained
{1}{B}{G}: /name/ fights another target creature.

## Counter spell (25)

Counter target spell

## Destroy (105)

Destroy target tapped creature
Destroy target permanent an opponent controls
Destroy target creature
Destroy target artifact
Destroy target land

# Exile (190)

Exile target card from a graveyard

## Pay more mana (76)

"pays" or "pay"

Quench
unless its controller pays {2}

Archon of Absolution
unless their controller pays {1} for 

## Reduce damage

Angel of Grace
When /name/ enters the battlefield ON_ENTER,A , until end of turn, damage that would reduce your life total to less than 1 reduces it to 1 instead.

## Protection

Apostle of Purifying Light
Protection from black (This creature can't be blocked, targeted, dealt damage, enchanted, or equipped by anything black.)


## xxx and yyy, xxx or yyy

Athreos, Shroud-Veiled
...dies ON_DIE,H or is put into exile

Kroxa, Titan of Death's Hunger
Whenever /name/ enters the battlefield or attacks


## Exile to hand

Bag of Holding
Return all cards exiled with /name/ to their owner's hand

## Non land mana

Seasonal Ritual
Add one mana of any color