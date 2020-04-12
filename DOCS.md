

    cur.execute("""SELECT DISTINCT name, text, manaCost,
                        (SELECT scryfallId FROM cards c2 WHERE c1.name=c2.name AND c2.setCode IN ('GRN', 'RNA', 'WAR', 'M20', 'ELD', 'THB') LIMIT 1) AS scryfallId 
                   FROM cards c1 WHERE setCode in ('GRN', 'RNA', 'WAR', 'M20', 'ELD', 'THB')""", [])
    for card in cur.fetchall():
        analysis = get_card_analysis(nlp, card, False)
        insert(savecur, card["name"], analysis)
