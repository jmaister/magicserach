

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