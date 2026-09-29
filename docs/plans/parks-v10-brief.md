# Brief — Parks v10 « National Park » : la première version jouable

(Le prompt de lancement de l'agent de construction, gardé ici : relis-le après chaque reprise de
contexte.)

Tu reprends Hearthlight, un jeu cozy en pixel art 2.5D : Three.js, tout procédural, sans build,
solo et Party Mode de 1 à 8 joueurs avec les téléphones comme manettes. Un nouveau mode a été
préparé, **« National Park »** : se balader dans les 63 parcs nationaux américains, recréés dans
le style du jeu.

Ta mission : sa **première version jouable, en local seulement**. Rien n'est déployé, rien n'est
publié. Travaille en autonomie, sans poser de questions : décide, documente tes choix, et continue
jusqu'à ce que tout soit à **9/10 minimum** (voir la grille plus bas). Termine par un résumé en
français (voir « À la fin »).

## L'esprit du mode (la vision de l'utilisateur)

- **Chill.** Pas d'histoire, pas de combat, pas de niveaux : se balader avec ses amis, découvrir,
  profiter. C'est un « walking simulator » partagé, et l'expérience passe avant tout.
- **Réaliste.** Quelqu'un qui a déjà vu le parc doit **reconnaître** sans étiquette les routes,
  les chemins et les lieux phares.
- **On s'y déplace comme un visiteur** : un van pour rouler sur les routes du parc, la navette là
  où le parc en a une.
- **On y vit le parc** : ses animaux emblématiques, des activités réelles, et des découvertes et
  des easter eggs cachés un peu partout.
- **Une carte des États-Unis** façon carte du monde de Mario, avec les parcs en grands points
  d'intérêt. On apparaît dans un parc, et on en sort par une entrée ou depuis le menu pour en
  choisir un autre.
- **Trois façons de jouer** : en solo, en Party (canapé + téléphones), ou dans un monde ouvert
  partagé où tous les joueurs connectés se voient. Le monde ouvert est le mode par défaut ; pour
  l'instant, il tourne en local.

## Avant de toucher au code

1. **Lis**, dans cet ordre :
   - `CLAUDE.md` ;
   - **en entier**, `docs/plans/parks-v10.md` :
     - §0 d'abord : les règles de publication ;
     - §3–§5 : les trois façons de jouer, les bulles, le serveur ;
     - §6.3 : la carte des USA ;
     - §7 : de la carte des visiteurs à la carte du jeu, dont §7.7 (les systèmes communs) et §7.8
       (le réalisme) ;
     - §8 : ce que font les joueurs ;
     - §10.1 : la grille de notes ;
   - `docs/parks/README.md` ;
   - `docs/parks/zion.md`, ta bible pour Zion ;
   - `docs/parks/SOURCES.md` et `docs/parks/refs/ZION.json` ;
   - `docs/ONLINE.md` et `server/relay.mjs`, le modèle du futur serveur du monde.
2. **Isole-toi.** L'utilisateur et d'autres agents (dont Codex) travaillent dans
   `~/Github/hearthlight-public`, avec des fichiers non commités : n'y travaille pas.
   - Fais ton propre clone (ou worktree) de `Hearthlight/hearthlight.github.io`, sur une
     **branche `parks-v10`**.
   - Utilise l'identité noreply du repo : `git config user.name pookee` et
     `git config user.email 13053375+pookee@users.noreply.github.com`.
   - Lance ton serveur de test sur un port libre (ni 8765 ni 8766), et ouvre toujours le jeu muet
     (`&mute=1`) : l'utilisateur travaille à côté.
3. **Récupère Zion.**
   - Les données : `python3 tools/parks/fetch.py --only ZION`.
   - Les photos de référence : `python3 tools/parks/fetch.py refs --only ZION`. Elles arrivent dans
     `tools/parks/cache/ZION/refs/` (git-ignoré) avec un index.
   - **Regarde chaque photo (outil Read) avant de modéliser le lieu qu'elle montre.**
   - Lis aussi la brochure officielle de Zion (liens dans la fiche) : rends-la en image et
     regarde-la zone par zone.
4. **Joue et mesure l'existant** (solo, Party avec bots), et note l'état de départ de chaque aspect
   de la grille.

## Règles non négociables

- **Rien de public, rien de jouable** (plan §0) :
  - Tu travailles et tu pousses sur la branche `parks-v10`. **Ne fusionne jamais dans `main`**
    sans l'accord explicite de l'utilisateur. Fusionne régulièrement `origin/main` dans ta branche
    pour rester à jour.
  - Dès le premier commit, le mode n'est accessible que derrière un drapeau local : `?parks=1`,
    honoré seulement avec `?debug=1` sur `localhost`.
  - Dès le premier commit aussi, `.github/workflows/pages.yml` et `desktop/scripts/copy-game.mjs`
    excluent `src/parks/` et tout futur fichier du mode. Une vérification échoue si le mode se
    glisse dans une de ces copies.
  - Le serveur du monde (`server/world.mjs`) tourne **en local uniquement** : aucun déploiement,
    aucune URL publique dans `config.js`, rien sur le VPS.
- **Chaque push est audité** (plan §0) :
  - rien de secret, aucune adresse d'infrastructure privée, aucune donnée personnelle, aucun
    chemin local, aucun texte ni image copiés ;
  - cherche dans les fichiers ajoutés toute trace personnelle : le vrai nom ou l'e-mail de
    l'utilisateur, les chemins de son disque (`/Users/…`, `/private/tmp`, les dossiers de travail),
    l'adresse IP du VPS, les e-mails, les IP, et les mots key, token et secret ;
  - `git add` seulement tes propres chemins.
- **Les photos de référence ne sortent jamais du cache** : jamais commitées, jamais dans le jeu,
  jamais montrées aux joueurs. Le jeu reste 100 % procédural : aucun fichier image ou audio.
- **Les règles de `CLAUDE.md`** :
  - pixels nets, toon, police pixel, panneaux papier, sons synthétisés ;
  - chaque texte visible passe par `t('English', vars)`, avec le français, l'espagnol, l'allemand
    et l'italien (`node tools/i18n-scan.mjs` : **0 missing** partout) ;
  - jamais une touche écrite en dur dans une aide : `ctl()` ;
  - 0 erreur dans la console et dans `window.__errs` ;
  - jamais de variable `t` ;
  - solo, Party et monde ouvert partagent leurs systèmes et doivent tous marcher : teste les trois,
    avec 1, 4 et 8 bots.
- **La vérité et le respect** :
  - les noms et les faits sont réels, tirés de la fiche ;
  - pas d'emblème NPS, et les noms du jeu sont « Park Passport » et « Young Ranger » ;
  - aucune position pour un lieu fermé ou fragile ;
  - les lieux et l'histoire amérindienne sont racontés comme le parc les raconte.

## Ce que je veux

### 1. La messagerie, dans tous les modes (à faire en premier)

Tout le plan §4 :
- **Téléphone** : une feuille avec le clavier du téléphone (80 caractères), les phrases rapides
  (12 par page, 3 pages), les émotes et l'historique. Pendant qu'on écrit, un « … » flotte
  au-dessus du héros.
- **Clavier** : `ctl('chat')` (T) ouvre une ligne de chat dans la vue du joueur.
- **Manette** : une roue de phrases et d'émotes (Y), et le clavier à l'écran.
- **Jeu à distance** (`play.html`) : une zone de texte.
- **Affichage** : une bulle au-dessus de la tête, qui dure selon la longueur du message, et un
  journal.
- **Langues** : les phrases rapides partent sous forme d'identifiant, et chacun les lit dans sa
  langue. Les émojis deviennent des émotes.
- **Sécurité** (plan §5.7) :
  - un filtre et des limites de débit ;
  - sourdine, blocage et signalement (dans un journal local pour l'instant) ;
  - un réglage familial « phrases rapides seulement ».

La messagerie doit aussi marcher dans le Party Mode actuel et en solo, pas seulement dans
National Park.

### 2. Le moteur des parcs

- **Un parc est une grande instance extérieure**, hors du monde principal, avec sa taille, sa
  palette, sa météo et son heure (la technique de `src/saga/instance.js`). Le streamer, le peintre
  en workers, la collision et la minicarte prennent un descripteur de carte au lieu de la
  constante `BIG`.
- **Le format de données d'un parc** : `src/parks/data/<code>.js`, décrit au plan §7.2.
- **Les outils qui le préparent** (plan §7.3), autant qu'ils t'aident :
  - le relief, depuis l'USGS 3DEP (domaine public) ou les tuiles de terrain AWS ;
  - la déformation « rubber sheet » ;
  - une ébauche et un aperçu PNG à comparer à la brochure.

  Ensuite, une passe à la main.
- **La découpe caméra** des bords de canyon et des feuillages (plan §7.7, point 1), et **la
  caméra de belvédère**. Sans elles, Zion est illisible : la caméra regarde vers le nord, donc les
  parois sud cachent le fond du canyon.
- **Les parois de 600 m.** Aujourd'hui le relief a 8 niveaux (0 à 7). Décide comment rendre les
  grands murs de Zion lisibles et beaux (plus de niveaux, des faces en 3D, des pièces de falaise),
  et note ta décision.

### 3. Zion, complet et reconnaissable

Suis `docs/parks/zion.md` (sa partie « For the game » propose une carte de 1024 × 1024 tuiles) et
les photos de référence. Au minimum :

- **Zion Canyon** :
  - la North Fork de la Virgin River ;
  - le Zion Canyon Scenic Drive et ses **9 arrêts de navette** : Visitor Center, Zion Human History
    Museum, Canyon Junction, Court of the Patriarchs, Zion Lodge, The Grotto, Weeping Rock, Big
    Bend, Temple of Sinawava ;
  - le Pa'rus Trail (à vélo aussi) ;
  - Zion Lodge et sa pelouse, les campings Watchman et South, le Nature Center.
- **Les lieux phares**, reconnaissables au premier coup d'œil :
  - The Watchman, avec la vue classique au couchant depuis les passerelles du Pa'rus près de
    Canyon Junction ;
  - la Court of the Patriarchs, le Great White Throne, les Towers of the Virgin, le West Temple ;
  - **Angels Landing** : Walter's Wiggles, Scout Lookout, les chaînes ;
  - les **Emerald Pools** (inférieure, du milieu et supérieure) ;
  - **Weeping Rock** et ses jardins suspendus ;
  - le **Riverside Walk**, puis **les Narrows**, où l'on marche dans la rivière, jusqu'à Wall
    Street.
- **Le côté est** : la Zion–Mount Carmel Highway et ses lacets, **le tunnel** de 1,8 km avec ses
  fenêtres, le Canyon Overlook Trail et sa vue, **Checkerboard Mesa**, l'East Entrance.
- **Les bords** : Springdale et l'entrée piétonne ; les Kolob Canyons (Timber Creek Overlook) et la
  Kolob Terrace comme la fiche le propose, en coins compressés (une deuxième passe si besoin).
- **Se déplacer comme un visiteur** :
  - à pied et à vélo ;
  - **en van** sur la route de l'est, le tunnel et Kolob. Vraie règle depuis juin 2026 : les
    véhicules trop grands sont interdits dans le tunnel ; le van doit être à la bonne taille ;
  - **en navette** dans le canyon. Le Scenic Drive est fermé aux voitures en saison : on gare le
    van et on prend la navette, avec les arrêts annoncés.
- **Les animaux emblématiques**, vivants et prudents : ils réagissent à la distance (plan §8.6).
  - Cerfs mulets, mouflons du désert côté est, dindons sauvages, rainettes des canyons, lézards à
    collier.
  - **Condors de Californie**, avec leur numéro de bague.
  - Écureuils des rochers : on ne les nourrit pas, ils mordent.
  - La nuit, le ringtail, et les tarentules en automne.
- **Des activités réelles** :
  - les randonnées ;
  - marcher dans les Narrows, avec le vrai risque de crue éclair et la vraie règle de fermeture ;
  - la **loterie des permis d'Angels Landing** (résultats à 16 h) ;
  - le mode photo et les cartes postales ;
  - les causeries du ranger ;
  - le camping et les étoiles (Zion est un Dark Sky Park) ;
  - le Park Passport et ses tampons au visitor center ;
  - le guide de terrain, l'herbier et un livret Young Ranger.
- **Les moments** : le Watchman qui s'embrase au couchant, les cascades éphémères de la mousson, la
  neige sur le grès rouge, les couleurs d'automne, les condors dans les thermiques.
- **Les découvertes et les easter eggs** (plan §8.8) : au moins 30 à Zion, avec un compteur dans le
  journal. Par exemple :
  - des alcôves et des jardins suspendus, Kolob Arch ;
  - un condor bagué, une tortue du désert après la pluie ;
  - l'histoire du tunnel et des CCC ;
  - et quelques clins d'œil discrets au monde de Hearthlight.
- **Le jour et la nuit, la météo et les saisons** (plan §7.7, point 4).

### 4. La carte des États-Unis

Tout le plan §6.3 :
- **La carte** : les États-Unis dessinés en code façon carte du monde de Mario. Les contours
  viennent des fichiers du Census (domaine public), simplifiés en polylignes compactes.
- **Les parcs** : les 63 en grands points d'intérêt, chacun avec un petit monument. Zion est
  ouvert, les autres sont marqués « bientôt ».
- **Entrer et sortir** : le van roule de point en point. On entre dans Zion par son entrée
  principale. On en sort par une entrée (la barrière s'ouvre sur la carte) ou par le menu
  « Changer de parc ».
- **En monde ouvert**, la carte montre combien de joueurs sont dans chaque parc, et où sont ses
  amis.

### 5. Le moteur du monde partagé, en local

Tout le plan §5 :
- **`server/world.mjs`** :
  - des instances par parc, et l'intérêt par chunk ;
  - des ticks à 10 Hz ;
  - l'horloge commune : animaux, rangers, météo et moments se calculent à partir de la graine et
    de l'heure du serveur ;
  - des accessoires d'instance avec une durée de vie (feux de camp, tentes) et des compteurs
    communautaires ;
  - des jetons de reprise, des limites et une validation, un protocole versionné, `/health` et
    `/stats`.
- **Le client** :
  - l'interpolation des autres joueurs ;
  - un niveau de détail et un plafond pour 40 avatars et plus ;
  - les plaques de nom, les émotes, les bulles.
- **Le « foyer »** : une partie Party rejoint le monde ouvert ensemble.
- **Le repli hors ligne** : si le serveur est injoignable, c'est le même parc en solo ou en Party.
- **Les tests** :
  - `server/world.test.mjs` ;
  - `server/worldload.mjs`, avec 1 000 bots dans 20 instances ;
  - `tools/parkbots.js`, des bots dans le navigateur ;
  - des tests de chaos : tuer et relancer le serveur, perdre des paquets, ajouter de la latence.

Tout tourne sur `localhost` : **rien n'est déployé**.

## La grille de notes : continue jusqu'à 9/10 partout

C'est la grille du plan §10.1. Les aspects notés sont :
- reconnaissable ;
- carte fidèle ;
- beau ;
- sensations ;
- vivant ;
- découvertes et activités ;
- carte des USA ;
- monde partagé ;
- messagerie ;
- performance ;
- qualité.

Comment l'appliquer :
- **Avant de commencer**, note chaque aspect (0 pour ce qui n'existe pas encore).
- **Après chaque jalon**, note chaque aspect /10 honnêtement, avec des preuves : des captures, les
  chiffres des tests. Puis corrige et recommence, **jusqu'à 9 ou plus partout**.
- **Le test de reconnaissance.** Pour chaque vue de `refs/ZION.json`, fais une capture depuis le
  même endroit et dans la même direction, et compare les deux côte à côte (en local, jamais
  commité). Corrige jusqu'à ce qu'un visiteur dise « c'est le Watchman depuis le pont ».
- **Le journal.** Tiens `docs/plans/parks-v10-progress.md` : les notes, les décisions et ce qui
  reste, à jour à chaque jalon, pour pouvoir reprendre après une perte de contexte. Tiens aussi
  une revue de designer par aspect, comme `docs/plans/world-v7-reviews.md`.
- **Les captures.** Envoie-les à l'utilisateur au fil de l'eau (SendUserFile), prises avec la
  vraie caméra et au vrai zoom.

## Jalons proposés (l'ordre est à toi)

- **M0** : la sécurité — la branche, le drapeau, les exclusions Pages et desktop avec leur
  vérification, le journal, la grille à l'état de départ.
- **M1** : la messagerie, dans le Party et le solo actuels.
- **M2** : le moteur des parcs, la découpe caméra et une ébauche du terrain de Zion, avec des
  captures à côté de la brochure et des photos.
- **M3** : Zion complet en solo et en Party : routes, navette, van, sentiers, lieux phares,
  animaux, activités, découvertes, moments.
- **M4** : le monde partagé en local, le foyer, les bots, les tests de charge et de chaos.
- **M5** : la carte des États-Unis, et le passage d'un parc à l'autre.
- **M6** : le polissage, jusqu'à 9/10 partout.

Après **chaque** jalon :
- les tests : en solo, en Party avec 1, 4 et 8 bots, et le monde partagé avec des bots ;
- 0 erreur, 0 missing ;
- les captures et les notes ;
- l'audit de sécurité ;
- un commit, avec un message terminé par la ligne
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, et un push **sur la branche
  `parks-v10`** ;
- le journal et `CLAUDE.md` à jour : l'arborescence, les commandes, les pièges.

Le jeu existant doit rester intact et jouable à chaque commit.

## À la fin

Un résumé en français :
- ce qui est fait ;
- les notes /10 par aspect ;
- ce qui reste ;
- **comment l'essayer en local** : les commandes, l'URL avec le drapeau, et comment lancer le
  serveur du monde et des bots ;
- ce qu'il faudrait pour le publier un jour. C'est l'utilisateur seul qui en décidera.
