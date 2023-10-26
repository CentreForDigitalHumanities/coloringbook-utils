Input van het script:

1. Een CSV-bestand met gegevens over de deelnemers, met onder andere een kolom "Deelnemernaam".
2. Een download van Coloring Book, variant "final".
3. Een optie "any color". Als deze optie wordt aangezet, maakt het niet 
uit of de kleur van een vakje hetzelfde is als de verwachting, als het 
vakje maar is ingekleurd.

Stap 1: controle van de expectations.

Het script loopt door de CB-download heen en telt
- voor iedere survey, het aantal unieke pages;
- voor iedere page, het aantal unieke vakjes met een expectation;
- voor iedere expectation, hoe vaak die juist is gekleurd en hoe vaak 
niet of onjuist (rekening houdende met "any color").

(Noot voor de scriptontwikkelaar: het is handig om dit stadium ook alvast een opzoektabel te maken van de unieke combinaties van subject en name, en van de unieke combinaties van subject en survey met daarbinnen alle inkleuringen. In die laatste tabel kunnen de inkleuringen met "white" als color worden weggelaten, want dit betekent dat de deelnemer het betreffende vakje uiteindelijk weer heeft uitgegumd. Dat telt dus als niet ingekleurd.)


Ter controle laat het script aan de gebruiker zien
- het aantal gevonden pages per survey;
- pages die geen expectation (lijken te) hebben (dit kan ook gebeuren 
als er wel een expectation is, maar geen enkele proefpersoon die heeft 
ingekleurd);
- pages die meer dan één expectation hebben, met de naam en de verwachte 
kleur van iedere expectation;
- voor vakjes die vaker niet dan wel juist zijn ingekleurd, het precieze 
aantal juiste en onjuiste inkleuringen.

Dit overzicht kan voor de gebruiker aanleiding zijn om de expectations aan te passen en de 
data opnieuw te downloaden van Coloring Book. De gebruiker krijgt de 
keuze tussen stoppen en doorgaan (stoppen is noodzakelijk als er pages 
zijn met meer dan één expectation). Als alles er goed uitziet, kiest de 
gebruiker voor doorgaan en volgt stap 2. Anders kan de gebruiker na het 
opnieuw downloaden van de data opnieuw het script starten.

Stap 2: controleren en matchen van de namen van de proefpersonen.

Het script verzamelt
- alle unieke combinaties van subject en name in de CB-download;
- alle unieke combinaties van rijnummer en name in het deelnemersbestand.


Ter controle laat het script aan de gebruiker zien
- het aantal unieke subjects in de CB-download;
- het aantal rijen in het deelnemersbestand;
- of er meerdere subjects in de CB-download zijn met dezelfde name, en 
zo ja, welke;
- of er meerdere rijen in het deelnemersbestand zijn met dezelfde naam, 
en zo ja, welke;
- of er names zijn in de CB-download die niet voorkomen in het 
deelnemersbestand, en zo ja, welke;
- of er names zijn in het deelnemersbestand die niet voorkomen in de 
CB-download, en zo ja, welke.

De gebruiker krijgt opnieuw de kans om te stoppen.

Kiest de gebruiker voor doorgaan, dan kan die invoeren welke 
niet-matchende namen bij elkaar horen, en daarbij aangeven wat de juiste 
naam is. De gebruiker mag ervoor kiezen om namen die wel in de CB-download voorkomen maar niet in het deelnemersbestand, weg te laten in plaats van te matchen; die deelnemers worden dus weggelaten in de uiteindelijke uitvoer. Overtollige namen in het deelnemersbestand (als die er zijn) worden simpelweg niet gebruikt.

Stap 3: combineren van de gegevens.

Het script maakt een nieuwe tabel met daarin precies één rij voor elke 
unieke combinatie van subject, survey en page (als een subject heeft 
deelgenomen aan een survey, maar niets heeft ingekleurd in een page die 
bij die survey hoort, wordt er als nog een rij toegevoegd voor die 
combinatie van subject, survey en page). De kolommen zijn, van links 
naar rechts:

- subject
- nameCB (name afkomstig uit CB-download)
- survey
- nameExcel (naam afkomstig uit deelnemersbestand)
- overige kolommen uit het deelnemersbestand (zie voorbeelduitvoer)
- page
- expected word (naam van een vakje)
- chosen word (naam van een vakje)
- time
- color (werkelijk ingekleurd)
- expected (opgegeven verwachte inkleuring)
- category

Als expected word wordt altijd de naam gebruikt van het vakje waarvoor 
een verwachting is ingevuld. Als dit niet voorkomt in de data, en de 
gebruiker ervoor heeft gekozen om dit zo te laten, is deze cel leeg.

Als het vakje van het expected word is ingekleurd, is het chosen word 
identiek aan het expected word. Ingekleurd met "white" telt hierbij niet. Als dat niet zo is, maar andere vakjes 
op dezelfde page wel zijn ingekleurd, is het eerst ingekleurde vakje het 
chosen word (dwz de inkleuring met de laagste waarde voor de time-kolom, voor de gegeven combinatie van survey, subject en page). Is er helemaal geen vakje ingekleurd op de page, dan wordt het chosen word "skipped".

De time is de inkleurtijd die hoort bij het vakje van het chosen word. 
Als er geen chosen word is, blijft de cel van de time leeg.

De color hoort eveneens bij het vakje van het chosen word, en kan dus 
leeg zijn.

De expected is de kleur die hoort bij het expected word. Als er geen 
expected word is, is de cel van de expected (color) dus ook leeg.

De inhoud van de category-cel hangt af van de optie "any color". Als die 
optie uit staat, is de category gelijk aan wat er in de CB-download 
staat. Heeft de deelnemer niets ingekleurd op een pagina, dan hangt het 
ervan af of er een verwachting is opgegeven; zo ja, dan is de category 
"not_expected", anders "unspecified". Dit is conform de "compared to 
expected" downloadoptie. Als "any color" aan staat, worden "expected" en 
"miscolored" omgezet in "1" en alle andere categories in "0".

Stap 4: uitvoer en einde.

Het script produceert twee nieuwe CSV-bestanden:
- Een overzicht van de mismatchende names, hoe die zijn gekoppeld en wat 
de juiste name zou zijn, zoals door de gebruiker ingevoerd in stap 2.
- De samengevoegde tabel uit stap 3.