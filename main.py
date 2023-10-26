import streamlit as st
from streamlit_lottie import st_lottie

from src.confetti import load_lottieurl
from src.gpt import get_completion

questions = {
    1: "Befindet sich Ihr Dauergrünland in einem umweltsensiblen Bereich oder in Feucht- und Moorgebieten?",
    2: "Haben Sie bereits eine Genehmigung zur Umwandlung beantragt oder wurden Ihnen andere Rechtsvorschriften oder Verpflichtungen auferlegt, die einer Umwandlung entgegenstehen?",
    3: "Ist der Dauergrünlandanteil in Ihrer Region in den letzten Jahren um mehr als 4 Prozent gesunken?",
    4: "Handelt es sich bei Ihrem Dauergrünland um einen Grünlandlebensraumtyp des Anhangs I der FFH-Richtlinie?",
    5: "Haben Sie die Bereitschaft, an anderer Stelle in derselben Region eine Ersatzfläche für Dauergrünland anzulegen?",
    6: "Falls die Fläche nicht in Ihrem Besitz ist, haben Sie die Zustimmung des Eigentümers zur Neuanlage dieser Fläche als Dauergrünland?",
    7: "Können Sie nachweisen, dass die Fläche, die Sie als Dauergrünland neu anlegen wollen, mindestens fünf Jahre für den Anbau genutzt wird?",
    8: "Handelt es sich um Flächen, die im Rahmen von GAP-Maßnahmen entstanden sind oder erst ab 2015 neu entstanden sind?",
    9: "Haben Dauergrünlandflächen, die neu angelegt wurden, mindestens fünf Jahre für den Anbau gedient?",
    10: "Haben Sie Dauergrünland ohne Genehmigung umgewandelt, das ab dem 1. Januar 2021 neu entstanden ist?",
}


# Funktion, um die Benutzerantworten zu speichern
def save_responses(answers):
    prompt = f"""Du sollst meine Antworten für einen Fragebogen auswerten und bestimmen, ob ich förderungsberichtigt bin. 
Falls ich nicht förderungsberichtigt bin, gebe mir eine Begründung in Stichpunkten.
Bitte gebe NUR dein Ergebnis und - falls ich nicht förderberechtigt bin - die Begründung zurück und keinen weiteren Text. Z.B.: So:
"Du bist leider nicht förderungsberechtigt, weil:
* (1) Deine Antwort auf Frage 1 war Nein, was bedeutet dass <Begründung zu Frage 1>"

Die Grundlage für die Bewertung ist folgender Text:
```Ab dem Jahr 2023 werden wesentliche Verpflichtungen aus dem Greening der Jahre
2015 bis 2022 zum Erhalt des Dauergrünlandes bei der Konditionalität fortgeführt.
8
Umwandlung von Dauergrünland grundsätzlich nur mit Genehmigung
Dauergrünland darf grundsätzlich nur mit Genehmigung in andere Nutzungen umgewandelt werden.
Hinweis: Für Dauergrünland, das zu dem umweltsensiblen Dauergrünland gehört
(siehe dazu Regelungen zu GLÖZ 9) oder in Feucht- und Moorgebieten liegt (siehe
dazu Regelungen zu GLÖZ 2) gelten zusätzliche Anforderungen.
Die Genehmigung ist bei den zuständigen Stellen der Länder mittels der dort bereitgestellten Formulare zu beantragen. Eine Genehmigung wird nicht erteilt, wenn andere Rechtsvorschriften oder Verpflichtungen des Landwirts gegenüber öffentlichen
Stellen einer Umwandlung entgegenstehen oder der Dauergrünlandanteil in der Region um mehr als 4 Prozent abgenommen hat. Die zuständige Behörde gibt im Bundesanzeiger bekannt, falls es zu einer solchen Abnahme um mehr als 4 Prozent gekommen ist. Eine noch nicht genutzte Genehmigung erlischt mit Ablauf des Tages
einer entsprechenden Bekanntmachung der zuständigen Behörden.
Eine Genehmigung wird ferner nicht erteilt, wenn das Dauergrünland ein Grünlandlebensraumtyp des Anhangs I der Richtlinie 92/43/EWG (FFH-Richtlinie) des Rates
vom 21. Mai 1992 zur Erhaltung der natürlichen Lebensräume sowie der wildlebenden Tiere und Pflanzen außerhalb der Gebiete ist, die in die Liste nach Artikel 4 Absatz 2 Unterabsatz 3 der Richtlinie 92/43/EWG eingetragen sind.
Genehmigung mit Verpflichtung zur Anlage einer Ersatzfläche
Im Regelfall wird eine Genehmigung nur erteilt, wenn an anderer Stelle in derselben
Region eine andere Fläche mit der entsprechenden Hektarzahl neu als Dauergrünland angelegt wird (Ersatzfläche). Diese Fläche kann auch bereits vorher für Gras
oder andere Grünfutterpflanzen genutzt worden sein (zum Beispiel als Ackergras),
aber sie darf noch nicht zu Dauergrünland geworden sein. Die Fläche gilt ab dem
Zeitpunkt der Neuanlage als Dauergrünland und muss ab dann mindestens fünf aufeinander folgende Jahre für den Anbau von Gras oder anderen Grünfutterpflanzen
genutzt werden.
Die Ersatzfläche ist spätestens bis zu dem der Genehmigung folgenden Schlusstermin für den Sammelantrag (15. Mai) anzulegen. Erfolgt die Anlage der Ersatzfläche
nicht bis zu diesem Termin, erlischt die erteilte Genehmigung.
Die Neuanlage kann auch durch einen anderen Betriebsinhaber erfolgen. Voraussetzung für die Genehmigung ist in diesem Fall eine Bereitschaftserklärung dieses anderen Betriebsinhabers zur Anlage einer entsprechend großen Dauergrünlandfläche.
Soweit die Fläche, die als Dauergrünland neu angelegt werden soll, nicht im Eigentum des Betriebsinhabers steht, ist darüber hinaus die Zustimmung des Eigentümers
zur Neuanlage dieser Fläche als Dauergrünland erforderlich. Weiterhin ist eine Erklärung des Eigentümers erforderlich, im Falle eines Wechsels des Besitzes oder des
Eigentums jeden nachfolgenden Besitzer und den nachfolgenden Eigentümer darüber zu unterrichten, dass und wie lange diese Fläche aufgrund der EU-rechtlichen
Vorgaben für den Anbau von Gras oder anderen Grünfutterpflanzen genutzt werden
muss.
Genehmigung ohne Verpflichtung zur Anlage einer Ersatzfläche
Eine Genehmigung ohne Verpflichtung zur Neuanlage von Dauergrünland wird erteilt, wenn das Dauergrünland im Rahmen von Agrarumwelt- und Klimamaßnahmen 
9
der zweiten Säule der Gemeinsamen Agrarpolitik (GAP) entstanden ist oder wenn
das Dauergrünland erst ab dem Jahr 2015 neu entstanden ist.
Eine besondere Regelung gilt allerdings, wenn das Dauergrünland zwar erst ab dem
Jahr 2015 entstanden ist, diese Neuanlage aber im Rahmen der Erfüllung von CrossCompliance- oder Greening-Verpflichtungen erfolgte. Diese Ersatz-Dauergrünlandflächen nach Cross Compliance oder aufgrund von Greening-Verpflichtungen müssen mindestens 5 Jahre lang für den Anbau von Gras oder anderen Grünfutterpflanzen genutzt werden. Erst nach diesen 5 Jahren kann eine Genehmigung zur Umwandlung dieses Dauergrünlandes erteilt werden, und zwar nur dann, wenn an anderer Stelle in derselben Region eine andere Fläche mit der entsprechenden Hektarzahl neu als Dauergrünland angelegt wird. Dabei gelten im Übrigen die gleichen Anforderungen wie im oben beschriebenen Regelfall.
Eine Genehmigung ohne Pflicht zur Neuanlage von Dauergrünland kann auch erteilt
werden, wenn die Nutzung der Fläche derart geändert werden soll, dass die Fläche
keine landwirtschaftliche Fläche mehr ist.
Ausnahmen von der Genehmigungspflicht
Dauergrünland, das ab dem 1. Januar 2021 neu entstanden ist, darf ohne Genehmigung umgewandelt werden. Die erfolgte Umwandlung ist dann bei Stellung des
nächsten Sammelantrages anzuzeigen.
Hinweis: Gegebenenfalls stehen einer Umwandlung im jeweiligen Fall andere rechtliche Regelungen entgegen. Es wird deshalb empfohlen, sich bei der Unteren Naturschutz- und Wasserbehörde des zuständigen Kreises oder der kreisfreien
Stadt.vor einer Umwandlung von solchem Dauergrünland über das Bestehen anderer
rechtlicher Regelungen, die einer eventuellen Umwandung entgegenstehen, zu informieren.
Die genannte Ausnahme von der Genehmigungspflicht gilt allerdings nicht für Dauergrünland, das ab dem 1. Januar 2021
- als Ersatzfläche angelegt,
- nach widerrechtlicher Umwandlung wieder rückumgewandelt,
- im Rahmen der Regelungen zum Greening als Ersatzfläche angelegt oder
rückumgewandelt wurde und nach diesen Vorschriften als Dauergrünland
gilt oder
- aufgrund einer EU-Förderung im Rahmen der Förderperiode bis 2022 (Verordnung (EU) Nr. 1305/2013) aus Ackerland entstanden ist.
Nicht der Genehmigung bedarf eine Umwandlung von maximal 500 Quadratmetern
Dauergrünland je Antragsteller innerhalb einer Region pro Jahr (Bagatellregelung).
Diese Bagatellregelung kommt allerdings nur zur Anwendung, solange der Dauergrünlandanteil in der betreffenden Region um nicht mehr als 4 Prozent abgenommen
und die zuständige Behörde dies im Bundesanzeiger bekannt gemacht hat```

Hier sind meine Antworten für den Fragebogen:

Beginne deine Antwort mit JA, wenn ich förderberechtigt bin.

    """

    for nummer, antwort in answers.items():
        prompt += f"{nummer}. Frage '{questions[nummer]}': {antwort}\n"

    # st.write("Prompt:", prompt)
    # print(prompt)

    # show a loading indicator
    with st.spinner("Warte auf Ergebnis der KI. Dies kann einige Minuten dauern..."):
        # get the result from the GPT-3 API

        confetti_lottie_url = "https://lottie.host/0d7d01d8-6979-4ea7-a9a1-60403b616093/PUGJ85OnDa.json"  # URL der Konfetti-Animation
        sad_lottie_url = (
            "https://lottie.host/bacfae90-69c3-47f2-8aa7-2d9025aba551/cu3n7q3ON0.json"
        )

        confetti_lottie_animation = load_lottieurl(confetti_lottie_url)
        sad_lottie_animation = load_lottieurl(sad_lottie_url)

        result = get_completion(prompt)

        # show reesult in the streamlit app
        st.write("Dein Ergebnis:", result)

        if result.startswith("JA"):
            st_lottie(confetti_lottie_animation, height=300, width=300)
        else:
            st_lottie(sad_lottie_animation, height=300, width=300)


def main():
    st.title("Dauergrünland-Umwandlungsanfrage")

    # Initialisieren eines leeren Wörterbuchs für die Antworten
    antworten = {}

    # Definition der Fragen

    # Erstellen der Ja/Nein Toggles für jede Frage
    # for nummer, frage in fragen.items():
    #     antworten[nummer] = st.radio(f"Frage {nummer}: {frage}", ('Ja', 'Nein'))

    # # Fragen mit Ja/Nein Optionen
    # antworten[1] = st.toggle(
    #     "1. Befindet sich Ihr Dauergrünland in einem umweltsensiblen Bereich oder in Feucht- und Moorgebieten?"
    # )
    # antworten[2] = st.toggle(
    #     "2. Haben Sie bereits eine Genehmigung zur Umwandlung beantragt oder wurden Ihnen andere Rechtsvorschriften oder Verpflichtungen auferlegt, die einer Umwandlung entgegenstehen?"
    # )
    # antworten[3] = st.toggle(
    #     "3. Ist der Dauergrünlandanteil in Ihrer Region in den letzten Jahren um mehr als 4 Prozent gesunken?"
    # )
    # antworten[4] = st.toggle(
    #     "4. Handelt es sich bei Ihrem Dauergrünland um einen Grünlandlebensraumtyp des Anhangs I der FFH-Richtlinie?"
    # )
    # antworten[5] = st.toggle(
    #     "5. Haben Sie die Bereitschaft, an anderer Stelle in derselben Region eine Ersatzfläche für Dauergrünland anzulegen?"
    # )
    # antworten[6] = st.toggle(
    #     "6. Falls die Fläche nicht in Ihrem Besitz ist, haben Sie die Zustimmung des Eigentümers zur Neuanlage dieser Fläche als Dauergrünland?"
    # )
    # antworten[7] = st.toggle(
    #     "7. Können Sie nachweisen, dass die Fläche, die Sie als Dauergrünland neu anlegen wollen, mindestens fünf Jahre für den Anbau genutzt wird?"
    # )
    # antworten[8] = st.toggle(
    #     "8. Handelt es sich um Flächen, die im Rahmen von GAP-Maßnahmen entstanden sind oder erst ab 2015 neu entstanden sind?"
    # )
    # antworten[9] = st.toggle(
    #     "9. Haben Dauergrünlandflächen, die neu angelegt wurden, mindestens fünf Jahre für den Anbau gedient?"
    # )
    # antworten[10] = st.toggle(
    #     "10. Haben Sie Dauergrünland ohne Genehmigung umgewandelt, das ab dem 1. Januar 2021 neu entstanden ist?"
    # )

    # Variable zur Überprüfung, ob alle Fragen beantwortet wurden
    alle_beantwortet = True

    # Erstellen der Ja/Nein Toggles für jede Frage
    for nummer, frage in questions.items():
        antwort = st.radio(
            f"Frage {nummer}: {frage}", ["Ja", "Nein", "Unbeantwortet"], index=2
        )

        # Überprüfen, ob die Frage unbeantwortet ist
        if antwort == "Unbeantwortet":
            # st.warning(f"Frage {nummer} ist unbeantwortet.")
            alle_beantwortet = False

        antworten[nummer] = antwort

    if st.button("Antworten speichern"):
        if alle_beantwortet:
            save_responses(antworten)
            st.success("Ihre Antworten wurden gespeichert.")
        else:
            st.error("Bitte beantworten Sie alle Fragen, bevor Sie fortfahren.")


if __name__ == "__main__":
    main()
