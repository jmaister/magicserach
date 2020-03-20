

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

# SEO

## tips

- Cambiar url de uuid a nombre de la carta


## Other

https://search.google.com/structured-data/testing-tool#url=https%3A%2F%2Fmagic.paellalabs.com%2Fsearch
https://search.google.com/structured-data/testing-tool

- Add "card analysis" to title

## SEO open graph

https://ogp.me/

## one

<meta property="og:site_name" content="San Roque 2014 Pollos">
<meta property="og:title" content="San Roque 2014 Pollos" />
<meta property="og:description" content="Programa de fiestas" />
<meta property="og:image" itemprop="image" content="http://pollosweb.wesped.es/programa_pollos/play.png">
<meta property="og:type" content="website" />
<meta property="og:updated_time" content="1440432930" />


## Complete


https://stackoverflow.com/questions/25100917/showing-thumbnail-for-link-in-whatsapp-ogimage-meta-tag-doesnt-work

<!-- MS, fb & Whatsapp -->

<!-- MS Tile - for Microsoft apps-->
<meta name="msapplication-TileImage" content="http://www.example.com/image01.jpg">    

<!-- fb & Whatsapp -->

<!-- Site Name, Title, and Description to be displayed -->
<meta property="og:site_name" content="The Rock Photo Studio">
<meta property="og:title" content="The Rock Photo Studio in Florida">
<meta property="og:description" content="The best photo studio for your events">

<!-- Image to display -->
<!-- Replace   «example.com/image01.jpg» with your own -->
<meta property="og:image" content="http://www.example.com/image01.jpg">

<!-- No need to change anything here -->
<meta property="og:type" content="website" />
<meta property="og:image:type" content="image/jpeg">

<!-- Size of image. Any size up to 300. Anything above 300px will not work in WhatsApp -->
<meta property="og:image:width" content="300">
<meta property="og:image:height" content="300">

<!-- Website to visit when clicked in fb or WhatsApp-->
<meta property="og:url" content="http://www.example.com">
