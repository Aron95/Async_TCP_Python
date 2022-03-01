# Async_TCP_Python


Gedanken zur Grundlegenden Kontrollstruktur für externe Netze:

Nachrichten die ein Server verarbeiten können muss:

    Anmeldung:

Aufbau:

String = “con,source ip, source port”

    Abmeldung:

Aufbau:

String = “dis,source ip, source port”

    Nachrichtensendung von Client zu Client:

Aufbau:

String ="sen, source ip, source port, destiny ip, destiny port, message"

    Adding:

Aufbau:

String ="add, source ip, source port, destiny ip, destiny port, message"

message kann in diesem Falle nur folgende 3 Zustände haben: -empty (bei erstanfrage) -acc (bei annahme) -rejc (bei ablehnung)

nicht erledigt: Späteres Featur: Ist die Anfrage rejctet gibt es ein Reject im Server, jede send Message wird vorher damit abgeglichen.

TODO: Konsequentzen aus diesen Nachrichten. Idee dazu: Entweder hat der Server oder der jeweilige Client eine Liste mit allen geaddeten Clients. Bei "sen"-Messages gehen nur die geaddeten Clients durch, der Rest wird verworfen.

Next TODO:

Logging implementieren! Funktionierende Register erdenken!
