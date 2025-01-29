# arbeidsgiver-datafortelling
Koden som genererer et [felles dashboard](https://data.ansatt.nav.no/productArea/2b4149d1-b18b-4111-923f-d7bcfdd55ba1) for PO Arbeidsgiver i Datamarkedsplassen.

# Oppsett
1. Installer Python3
2. Klon repoet og naviger til mappen
3. Opprett et virtuelt Python miljø: `python3 -m venv venv`
4. Aktiver det virtuelle Python miljøet: `source venv/bin/activate`
5. Installer avhengigheter: `pip3 install -r requirements.txt` ([quarto](https://quarto.org/) installeres automatisk)

## Gi tilgang til en ny person
1. Legg til personen i teamet `arbeidsgiver-data` i [nais console](https://console.nav.cloud.nais.io/team/arbeidsgiver-data/members).
    - Hvis du ser at noen har tilgang men ikke lenger jobber i PO-et, vær så snill og fjerne dem fra teamet i nais console.
2. Alle i PO Arbeidsgiver burde ha tilgang til GitHub-repoet, siden teamene er satt opp med tilgang til repoet. Dobbeltsjekk [her](https://github.com/navikt/arbeidsgiver-datafortelling/settings/access).

# Utvikling

1. Logg på Google Cloud: `gcloud auth application-default login`
2. Aktiver virtuelt Python miljø: `source venv/bin/activate`
4. Kjør `quarto run index.qmd` for å generere en lokal versjon av datafortellingen
5. Åpne `index.html` i nettleseren for å se resultatet: `open index.html`
6. Push endringer til github for å trigge bygg og deploy til NAIS
7. Kjør nais-jobben for å oppdatere dashboardet (se "Adhoc kjøring av naisjobben")

## Legge til ny metrikk i datafortellingen
1. Lage et view med metrikkene du trenger i [BigQuery](https://console.cloud.google.com/bigquery) ved å lagre en spørring som et view i teamets prosjekt
    - Vær oppmerksom: Ikke del hele datasettet/tabellen! Kun metrikker akkumuert på riktig nivå (uten personopplysninger eller andre info som ikke skal deles utenfor teamet ditt)
2. Autoriser BigQuery til å dele viewet ved å klikke på datasettet (ikke viewet/tabellen) i BigQuery, velge "Sharing", "Autorize Views" og så legge til viewet
3. Dele viewet med `arbeidsgiver-data@nav.no` i Datamarkedsplassen
    - [Opprett et nytt dataprodukt](https://data.ansatt.nav.no/dataproduct/new) om teamet ditt ikke har et allerede.
    - Eller legg til viewet som et datasett i et [eksisterende dataprodukt](https://data.ansatt.nav.no/user/products)
4. Nå er du klar til å lage en Python/Quarto-script. Hent dataene ved å opprette en klient med GCP-prosjektet `arbeidsgiver-data-prod-bb88` og kjøre en spørring, for eks: ``select * from `<teamets-prosjekt>.<datasett>.<view>` ``

## Deploy
Prosjektet bygges med github [workflow](https://docs.github.com/en/actions/writing-workflows/about-workflows) og deployes til NAIS som en [NAIS job](https://docs.nais.io/workloads/job/).

## Adhoc kjøring av naisjobben
NAIS-jobben kjører i forhold til en cronjob som er definert i [nais.yaml](https://github.com/navikt/arbeidsgiver-datafortelling/blob/main/.nais/nais.yaml). Hvis man ønsker å kjøre jobben i et annet tidspunkt, følg stegene under:

1. Logg inn i gcp: `gcloud auth login --update-adc`
2. Gå til cluster prod-gcp i kubectl: `kubectx prod-gcp`
3. Sett namespace: `kubens arbeidsgiver-data`
4. Finn cronjobben for datafortellingen: `kubectl get cronjobs | grep arbeidsgiver-datafortelling`
5. Husk å vente på at endringene er deployet før du kjører jobben
6. Trigg jobben: `kubectl create job --from=cronjob/arbeidsgiver-datafortelling arbeidsgiver-datafortelling-ad-hoc`
7. Du kan følge med på jobber [her](https://console.nav.cloud.nais.io/team/arbeidsgiver-data/prod-gcp/job/arbeidsgiver-datafortelling)

## Oppdater dashboardet manuelt, uten naisjobb
Ikke anbefalt, men mulig å bruke. 

1. Følg stegene i "Lokal utvikling" for å generere en lokal versjon av datafortellingen
2. Gjør miljøvariablene tilgjengelig:
    `export NADA_HOST=nada.ansatt.nav.no`
    `export QUARTO_ID=53cb8677-59b8-4de4-86bc-7bfff29d39cd`, datafortellingens id som finnes i lenken til datafortellingen og ikke er hemmelig
    `export TEAM_TOKEN=<team-token>`, team-token hentes i [Datamarkedsplassen secrets](https://data.ansatt.nav.no/user/tokens)
3. Kjør `curl -X PUT -F file=@index.html https://${NADA_HOST}/quarto/update/${QUARTO_ID} -H "Authorization:Bearer ${TEAM_TOKEN}"`

# Henvendelser
Spørsmål knyttet til koden eller prosjektet kan stilles som et [issue her på GitHub](https://github.com/navikt/arbeidsgiver-datafortelling/issues).
## For NAV-ansatte
Interne henvendelser kan sendes via Slack i kanalen #arbeidsgiver-utvikling eller #arbeidsgiver-general.

# Krediteringer
## Kode generert av GitHub Copilot
Dette repoet bruker GitHub Copilot til å generere kode.