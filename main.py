import streamlit as st


# Funktion, um die Benutzerantworten zu speichern
def save_responses(antworten):
    # Hier könnten Sie die Antworten speichern oder weiterverarbeiten
    # Zum Beispiel in einer Datei speichern oder in einer Datenbank
    pass


def main():
    st.title("Dauergrünland-Umwandlungsanfrage")

    # Initialisieren eines leeren Wörterbuchs für die Antworten
    antworten = {}

    # Fragen mit Ja/Nein Optionen
    antworten[1] = st.toggle(
        "1. Befindet sich Ihr Dauergrünland in einem umweltsensiblen Bereich oder in Feucht- und Moorgebieten?"
    )
    antworten[2] = st.toggle(
        "2. Haben Sie bereits eine Genehmigung zur Umwandlung beantragt oder wurden Ihnen andere Rechtsvorschriften oder Verpflichtungen auferlegt, die einer Umwandlung entgegenstehen?"
    )
    antworten[3] = st.toggle(
        "3. Ist der Dauergrünlandanteil in Ihrer Region in den letzten Jahren um mehr als 4 Prozent gesunken?"
    )
    antworten[4] = st.toggle(
        "4. Handelt es sich bei Ihrem Dauergrünland um einen Grünlandlebensraumtyp des Anhangs I der FFH-Richtlinie?"
    )
    antworten[5] = st.toggle(
        "5. Haben Sie die Bereitschaft, an anderer Stelle in derselben Region eine Ersatzfläche für Dauergrünland anzulegen?"
    )
    antworten[6] = st.toggle(
        "6. Falls die Fläche nicht in Ihrem Besitz ist, haben Sie die Zustimmung des Eigentümers zur Neuanlage dieser Fläche als Dauergrünland?"
    )
    antworten[7] = st.toggle(
        "7. Können Sie nachweisen, dass die Fläche, die Sie als Dauergrünland neu anlegen wollen, mindestens fünf Jahre für den Anbau genutzt wird?"
    )
    antworten[8] = st.toggle(
        "8. Handelt es sich um Flächen, die im Rahmen von GAP-Maßnahmen entstanden sind oder erst ab 2015 neu entstanden sind?"
    )
    antworten[9] = st.toggle(
        "9. Haben Dauergrünlandflächen, die neu angelegt wurden, mindestens fünf Jahre für den Anbau gedient?"
    )
    antworten[10] = st.toggle(
        "10. Haben Sie Dauergrünland ohne Genehmigung umgewandelt, das ab dem 1. Januar 2021 neu entstanden ist?"
    )

    if st.button("Antworten speichern"):
        save_responses(antworten)
        st.success("Ihre Antworten wurden gespeichert.")


if __name__ == "__main__":
    main()
