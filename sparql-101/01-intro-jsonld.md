# Modeling Semantic APIs

## Agenda

  - Semantics what?
  - Triples & co
  - Attaching semantics
  - Graph databases

*Beware*: commands contain small typos. You must fix them to properly complete the course!

---

## Intro: Semantics what?

Semantics: the study of meaning.

Semantics ensures that a message is understood.

```
name: Mario Romildo
```

Is this a given name or a full name?

----

La mancanza di standardizzazione nel formato e significato dei dati ostacola l’interoperabilità tra le basi di dati di enti diversi e quindi la creazione di servizi digitali.    

Un primo esempio è la mancanza di interoperabilità sintattica: una entità ben definita (eg. il codice fiscale) viene rappresentata con campi o formati diversi:

```
{"codice_fiscale": "MRORSS77T05E472W"}
{"cf": "mrorss77T05E472W"}
{"taxCode": "MRORSS77T05E472W"}
```

----

Un altro esempio è l'interoperabilità semantica: il concetto di famiglia ha diverse accezioni (eg. fiscale, anagrafica):

```
{"familiari": [{"nome": "Mario Rossi", "relazione": "padre"}, {"nome": "Carla Rossi", "relazione": "sorella" , "convivente": false}   }
{"familiari": [{"nome": "Mario Rossi", "relazione": "padre"}   }
```

---

## Semantic standardization

Per standardizzare semanticamente i servizi e i loro contenuti, si utilizzano strumenti concettuali quali ontologie e vocabolari controllati (codelist, tassonomie, ..). 

Ontologia: una ontologia è un insieme di assiomi logici che concettualizzano un dominio di interesse definendo dei concetti e la semantica delle relazioni tra essi. Quando le ontologie contengono ulteriori restrizioni (eg. vincoli allo schema) non sono propriamente vocabolari.


Vocabolario controllato: un vocabolario dove i termini sono validati da un'autorità designata. Può essere di diversi tipi - eg. una lista (codelist), una struttura gerarchica (tassonomia), un glossario ed un tesauro (che aggiunge ad una tassonomia ulteriori vincoli). Esempi di vocabolari controllati europei si trovano qui https://op.europa.eu/en/web/eu-vocabularies/controlled-vocabularies 

## Syntax standardization

Schema di dati: Uno schema è una rappresentazione/descrizione formale e machine-readable del contenuto effettivo o potenziale dei dati contenuti in un oggetto separato. In altre parole, è l'insieme di istruzioni semantiche e sequenziali che possono essere usate per controllare l'input memorizzato in un dato file, o per collegare un file che rispetta tali istruzioni a un sistema o un'applicazione di scambio di informazioni. Esistono diversi formati per descrivere degli schemi, tra cui xml-schema e json-schema. Definizione formale della sintassi di una entità. Vedi https://json-schema.org/understanding-json-schema/about.html 

Un Vocabolario controllato supporta anche la standardizzazione sintattica.

---

Per standardizzare sintatticamente i servizi serve pubblicare degli schemi dati a cui tutte le organizzazioni devono conformarsi. Storicamente la standardizzazione degli schemi dati si basa sul concetto di namespace eventualmente distribuiti - vedi il formato di specifica XSD.

Se in ecosistemi ben definiti questo approccio funziona, al crescere della dimensione si pongono una serie di problematiche legate sia alla compattezza dei dati trasportati che del contesto di sicurezza legato ad esempio alla eventuale necessità di dereferenziare gli URI (eg. https://owasp.org/www-pdf-archive/XML_Based_Attacks_-_OWASP.pdf ) .

Mentre poi la metadatazione delle pagine tramite json-ld ha come platea principale i sistemi di processamento batch dei motori di ricerca, i dati convogliati tramite API vengono sempre più frequentemente processati da applicazioni mobile che hanno dei vincoli sia in termini di banda che di consumo di risorse (eg. batteria dei cellulari, riscaldamento) più stringenti.

Inoltre la creazione di servizi sempre più integrati porta ad un aumento del numero di richieste, e della conseguente necessità di supportare in maniera sostenibile i carichi sui sistemi IT.


---

## Defining semantic contents

I contenuti semantici vengono definiti solitamente attraverso
delle proposizioni: `soggetto` `predicato` `complemento`

```
"il cane" "è" "nero"
"nero" "è" "un colore"
"il cane" "è" "un animale"
"un animale" "deve" "mangiare"
```

---

RDF: Resource Description Framework permette di rappresentare informazioni sul web basandosi su due strutture dati:
- grafi (insiemi di triple soggetto-predicato-oggetto) 
- elementi (IRI, blank e literals); 
e su dei vocabolari di elementi identificati tramite degli IRIs e dei namespace.

Un rdf-dataset è un insieme di grafi.

---

Esempio basato su quanto definito sopra

```
prefix animals: <https://animals.example>
prefix colors: <https://animals.example>

animals:dog colors:hasColor colors:black
colors:black a colors:Color
animals:dog a animals:Animal
```

---

Per standardizzare la semantica dei contenuti
digitali si usano delle Ontologie.

In Italia esiste l'Ontologia delle persone
che possiamo usare per descrivere univocamente
qualcuno.

```
@prefix cpv: <https://w3id.org/italia/onto/CPV> .

<email:robipolli@gmail.com> cpv:givenName "Roberto" .
<email:robipolli@gmail.com> cpv:familyName "Polli" .
                            
```
---

Anche l'ontologia è definita tramite triple
a partire da vocabolari di base.

```
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix dct:   <http://purl.org/dc/terms/> .

https://w3id.org/italia/onto/CPV dct:modified  "2020-04-27"^^xsd:date ;
https://w3id.org/italia/onto/CPV dct:title     "Person Ontology"@en, "Ontologia delle persone"@it ;

```

--- 

JSON-LD è un formato che permette di serializzare in JSON delle informazioni basate sul RDF data model.
 https://www.w3.org/TR/json-ld11/#data-model. 

Un documento JSON-LD è quindi sia un documento  RDF che JSON, e rappresenta un'istanza di un RDF data model. 

JSON-LD inoltre *estende* RDF per permettere la serializzazione di dataset RDF generalizzati. 
Di seguito l'estratto di sopra serializzato in JSON-LD/yaml.

```
"@context":
  cpv: "https://w3id.org/italia/onto/CPV" 
  given_name: "cpv:givenName"
  family_name: "cpv:familyName"
  id: "@id"
id: robipolli@gmail.com
given_name: Roberto
family_name: Polli
```

---

Oltre all'ontologia italiana, un altro vocabolario
molto usato sul web è www.schema.org. Le parole chiave
che definisce sono disponibili in formato json-ld 
https://schema.org/docs/jsonldcontext.jsonld 

---

È anche possibile ridefinire o localizzare i campi,
eventualmente usando diversi namespace.


```
"@context": 
  "sdo": "http://schema.org/"
  "nome":"sdo:name"
  "nome_proprio": "sdo:givenName"
"@type": "Person"
  "nome": "Jane Doe"
  "nome_proprio": "Jane"
  "sdo:jobTitle": "Professor"
  "sdo:telephone": "(425) 123-4567"
```

---

### Localizzazione

JSON-LD supporta nativamente informazioni
localizzate:

```
-- come lista
occupation:
-  @value: "Student"
   @language: en
-  @value: "Etudiant"
   @language: fr
```

oppure

```
-- come oggetto
@context:
  occupation:
    @container: @language
occupation:
  en: Student
  fr: Etudiant
```

oppure

```
--- tramite elementi multipli, utile anche per la serializzazione di API semplici 
@context:
  occupation: {@language: en}
  occupation_fr: {@language: fr} 
occupation: Student 
occupation_fr: Etudiant
```
--- 

Per validare un oggetto json-ld, serve risolvere 
ricorsivamente tutte le referenze:
è complesso farlo in maniera sincrona.

Quando si crea un API, la semantica va
essere definita in fase di specifica
in modo da non rendere necessaria la risoluzione
ed evitare problemi come il "@context mangling".




--




## API e Semantica

Quando scambiamo informazioni tramite API
la semantica non è sempre chiara:

- è implicita;
- è in qualche pdf/xls;
- non è machine readable.

---



```
!git init /repo-path
!ls -l /repo-path/.git  # this is the index directory
```

### Exercise

  - get the previous `git config ... user.email`  
  - remove the `--global` flag  from the previous command
  - run it

```
# Write here the command
# and show the git config file.
!cat .git/config
```
---

Enter in the repo directory and check  the status: there
are a lot of files we are not interested in...

```
!git status 
```

`.gitignore` lists the files we're not interested in

```
# Ignore all files not starting with h
!echo "[^h]*" >> .gitignore
!git status 
```

Now we have all `host*` files to be tracked.

---

## Populate the repo

Add files to the index

```
! git add hosts
```

The file is now *staged* for commit. It's not archived though.

```
!git status
```

Save files to the local index

```
! git commit -m "Initial snapshot of hosts"
```

![Git areas](https://git-scm.com/images/about/index1@2x.png)

---

## Basic workflow

Adding a line to the file we discover that

```
!echo "127.0.0.2  localhost2.localdomain" >> hosts 
!git diff hosts
```

If we like the changes, we can stage them 

```
!git add hosts
!git status 
```

and finally save them in the repo.

```
!git commit  "Added localhost2 to hosts"
```
---

## History changes

Now we have an history with two changes, containing:

 - commit messages
 - a commit hash

HEAD is the last commit.


```
!git log 
```

![Basic branch](https://git-scm.com/figures/18333fig0310-tn.png)

---

## Reverting changes

We can revert a change using the hash or an history log

```
! git checkout HEAD~1 -- hosts  # revert hosts to the previous commit
```

---

## Cheatsheet

Now some git commands, but first create a dir.

```
! mkdir -p /repo-path
!date >> /repo-path/file.txt
!date >> /repo-path/hi.txt
```
---

```
!git init /repo-path    # Initialize repo eventually creating a directory
!git add /repo-path/hi.txt # Add file to index
!git commit -m "My changes"  # Save changes
```

### Exercise

  - add `file.txt` to the index and commit

```
# Use this cell for the exercise
```

---


```
!date >> /repo-path/file.txt
!git diff
!git commit -a -m "Save all previously added files"
```

---


```
!git log /repo-path/file.txt  # show changes
```

```
!git checkout HEAD~1 -- file.txt # revert file
```

```
!git diff HEAD  # diff with reverted
```

```
!git checkout HEAD -- . # get *all files* from the latest commit
```

---

## Tags & Branches 

Writing codes and configuration we may want to follow
different strategies and save our different attempts.

  - *tag*  makes an unmodifiable snapshot of the repo instead.

```
!git tag myconfig-v1 # create a tag
!git tag -l    # list tags
```

  - *branch* create a modifiable copy of the code, allowing 
     to save and work on different features

![Branches](https://git-scm.com/figures/18333fig0313-tn.png)

---

## Branches

`master` is the default branch

```
!git branch -a
```

Create a branch

```
!git checkout -b work-on-my-changes
```

And list the branches, check the active one!

```
!git branch -a
```

---

Modify a file in a branch

```
!date > new-file.txt
!git add new-file.txt
```

With commit we consolidate the new file in the branch

```
!git commit -m "Added a new file"
```

---

Compare branches

```
!git diff mister
```

Diff supports some parameters

```
!git diff --ignore-all-space master
```

---

We can now switch between branches

```
!git checkout master
!cat new-file.txt
```

And switch back

```
!git checkout work-on-my-changes
!cat new-file.txt
```

---

### Exercise

  - Create a new branch named `antani`
  - modify `new-file.txt` as you please
  - open a terminal, and use `git add -p` to stage the changes. What does it do?
  - commit the changes

```
# Use this cell for the exercise
```

---

## Checkout troubleshooting

If you change a file, git won't make you checkout
to avoid missing changes.

```
!date >> new-file.txt
!git checkout master
```

You have to remove the changes or commit them (in another branch too)

```
# Use this cell for the exercise.
```


---

## Merge

Once we have consolidated some changes (Eg. test, ...)
we can *merge* the changes into the master branch

```
!git checkout master
!git diff work-on-my-changes
!git merge work-on-my-changes
```

---

After a merge, if the branch is no more useful, we can remove it.

```
!git branch -d work-on-changes
```

If there are unmerged changes, git doesn't allow deleting a branch.

Exercise:

  - use `git branch -d` to remove the `antani` branch
  - what happens?
  - replace `-d` with `-D`. Does it work now?

```
# use this cell for the exrcise

```

---

## Selective adding

You can stage partial changes with:

```
!git add -p 
```


---

## Remote repositories

Remote repos may be either https, ssh or files.


```
! mkdir -p /repo-tmp && cd /repo-tmp # use another directory
```

---

### https repo

Git clone downloads a remote repo, with all its changes and history.
Try with a remote https repo.

```
! git clone https://github.com/ioggstream/python-course/ python-course
cd /repo-tmp/python-course
```

Show repository configuration. Remote origin.

```
! git config -l 

```

The remote repo is retrieved with all its changes and history
```
! du -ms .git
```

And `log` can show branches and merges.

```
!git log --graph
```
---

### file repo

A local repo can be cloned too, and has the same features
of a remote one. It's actually a remote file:// uri.

```
! git clone /repo-tmp/python-course /repo-tmp/my-course
```

Show repository configuration. Remote origin.

```
! git config -l

```

---

## Pull & push

You can add new files to a repo with the above workflow:

  - create a branch with `git checkout -b test-1`
  - add a new file
  - stage changes with `git add`
  - commit with `git commit`

Now that your changes are on your local repo, you can synchronize / upload them to the remote copy
with:

```
! git push origin test-1
```

Remember:

  - origin is the URI specified by `git config -l`
  - `test-1` is the branch name where you want to upload

To upload changes to the remote master (default) branch, you need to

  - merge the changes to your local master

```
!git checkout master
!git merge test-1
```

  - push changes to master

```
!git push origin master
```

To make it work, you need to be authenticated/authorized with the remote repo ;)

