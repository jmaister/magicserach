

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

## Ravager Wurm

 /name/ fights target creature you don't control. • Destroy target land with an activated ability that isn't a mana ability.

## Escape
 
 Pharika's Spawn
 Escape—{5}{B}, Exile three other cards from your graveyard. (You may cast this card from your graveyard for its escape cost.)

## Jump start

 Jump-start (You may cast this card from your graveyard by discarding a card in addition to paying its other costs. Then exile this card.)

## Create copy 

Quasiduplicate
Create a token that's a copy of target creature you control.


## Counters 

+1/+1 counter
with an additional +1/+1 counter on it
/name/ escapes with a +1/+1 counter on it.
Woe Strider escapes with two +1/+1 counters on it.


## Adamant

Adamant - if at least...

## Sacrifice

sacrifice /name/

## Fight

Polukranos, Unchained
{1}{B}{G}: /name/ fights another target creature.
