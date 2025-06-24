# TP5-MicroService (Axel Pedrero / Simon Lours)

# Blagues.pdf

## Questions de compréhension

### Pourquoi faire des petits services ?

1. Pourquoi voudrait-on diviser un gros service web en plusieurs morceaux plus petits ?
   
   Pour gagner en modularité car chaque petit service est plus facil à comprendre, maintenir, tester et déployer. Cela permet d’isoler les changement sans impacter tout le système
   
2. Imaginez que vous travaillez sur un gros projet. Que se passe-t-il si vous devez modifier une seule fonctionnalité ? Est-ce facile ? Risqué ?
   
   Dans un gros projet, modifier une seule fonctionnalité peut être complexes et risqué, car cela peut avoir des impacts involontaires ailleurs
   
3. Peut-on confier un petit service à une autre équipe ou un autre développeur sans qu'il ait besoin de connaître tout le reste ?

   Oui, c’est un avantage clé des microservices car chaque service est autonome et on peut l’attribuer a une autre équipe ou a un développeur sans qu’ils ait à connaître tout le système
   
4. Que se passe-t-il si une partie tombe en panne ? Peut-on réparer sans tout redémarrer ?

   Oui, dans une architecture microservices, chaque service fonctionne de manière indépendante. Si un service tombe en panne, on peut le redémarrer ou le remplacer sans affecter les autres.
   
5. Avez-vous déjà vu ou utilisé un site ou une appli qui semblait "modulaire" ?

    Par exemple : Amazon ouNetflix où chaque fonctionnalité (paiement, catalogue, suggestions,...) semble être un module à part

### Comment découper un service ?

6. Sur quels critères peut-on séparer un gros service en plusieurs petits ?

   Par fonctionnalité (par exemple : blagues, météo, ...), par type de données manipulées, ou par responsabilités métiers distinctes
   
7. Faut-il découper par fonctionnalité (ex : blague, météo, ...) ? Par type de donnée ? Par public cible ?

   Il est généralement préférable de découper par fonctionnalité. Chaque microservice doit gérer une seule responsabilité claire. Mais les autres critères peuvent aussi être pertinents selon le contexte.
   
8. À partir de combien de lignes de code ou de routes HTTP faut-il envisager un découpage ?

     Il n’y a pas de règle fixe, mais si le code devient difficile à maintenir, tester ou comprendre, ou si le service a trop de routes HTTP, c’est un bon indicateur pour envisager un découpage.
    
9. Le découpage doit-il être figé ou peut-il évoluer ?

    Il doit pouvoir évoluer. L’architecture logicielle est vivante : les besoins changent, et l’organisation du code doit pouvoir s’adapter sans tout réécrire.
   
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Météo.pdf

**1. Pourquoi ne pas appeler directement open-meteo depuis le navigateur ?**


Sécurité : les appels directs du navigateur exposent la clé API (s’il y en avait une), ce qui peut poser des risques d’abus ou de piratage

Abstraction : cela permet de masquer la complexité de l’API externe et de fournir une interface plus simple aux utilisateurs internes.

Contrôle : cela permet de filtrer ou formater les données avant qu’elles ne soient utilisées

**2. Quel est l’avantage de passer par un microservice intermédiaire ?**

tout passe par un point unique, plus facile à maintenir. Simplification des appels pour les autres services ou développeurs (moins de paramètres, format unifié).
Possibilité d’ajouter du cache, des statistiques,...

**3. Si le format de réponse de open-meteo change, que se passe-t-il ?**

Si on appelle directement l’API depuis le front, tout casse 
Mais avec un microservice intermédiaire, on peut :

Adapter rapidement la structure du code backend,

Préserver l’interface fournie aux consommateurs

Cela isole les impacts du changement de format.

**4. Que pourrait-on ajouter pour rendre ce service plus complet ou plus
robuste ?**

Persistance des requêtes récentes (cache temporaire pour éviter les appels répétés)

Ajout d’une clé API personnelle pour accéder au service (gestion des droits d’accès)

Traduction automatique des conditions météo

Ajout des prévisions (pas juste la météo actuelle) sur 24h ou 7 jours


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Persistance-orm.pdf

**1. Pourquoi ajouter une base de données à un service météo aussi simple ? Est-ce justifié ?**

Cela permet d’éviter les appels redondants à l’API externe, en cachant les données. Même si le service est simple, ça améliore les performances, évite les bannissements, et illustre un usage typique d’architecture moderne

**2. Est-ce que chaque microservice devrait avoir sa propre base, ou peut-on les partager ?**

En architecture microservices, chaque service doit avoir sa propre base de données. Cela garantit l’indépendance et l’encapsulation des services. Partager une base casse ce principe et introduit du couplage

**3. Que gagne-t-on (et que perd-on) en utilisant une base relationnelle plutôt qu’un fichier ou un dictionnaire Python ?**

On gagne en structure, recherche rapide, concurrence maîtrisée, et persistance fiable.
On perd un peu en simplicité et performance brute pour des petits volumes

**4. Que permet une base comme MySQL que ne permet pas un fichier JSON ?**

MySQL permet des requêtes complexes (filtres, tris), accès simultanés sûrs, transactions, indexation, intégrité des données, et sauvegarde/restauration fiablee

**5. Si on voulait partager cette météo avec d’autres services, la base est-elle une bonne interface ?**

Non, la base ne doit pas être exposée directement. On passe par une API REST pour interagir avec elle, ce qui permet de contrôler l’accès, le format, la sécurité, etc......

**6. Peut-on facilement sauvegarder/exporter les données ? Et les restaurer ?**

Oui

**7. Est-ce que l’ajout d’une BDD rend le service plus rapide ? Plus lent ?**

Au départ un peu plus lent, car on ajoute une couche
Mais au global plus rapide car on évite de recontacter une API lente à chaque fois

**8. Que se passe-t-il si plusieurs clients envoient des requêtes simultanément ?**

Grâce à la BDD, les requêtes peuvent être gérées en parallèle sans conflit. Contrairement à un fichier, pas de risque d'accès concurrent mal géré

**9. Peut-on mettre à jour une donnée météo sans recontacter l’API externe ?**

Oui, il suffit de modifier directement l’entrée en base si on connaît les nouvelles valuers

**10. Est-ce qu’on peut interroger la météo d’hier ou de demain avec cette architecture ?**

Non, pas sans modification. L’API actuelle ne fournit que la météo actuelle, et la base ne stocke qu’un instant T. Il faudrait ajouter des horodatages multiples et un paramètre de date



### Question de rélfexion

**1. Pourquoi voudrait-on éviter d’écrire directement des requêtes SQL à la main ?**

Franchement, écrire du SQL à la main, c’est vite long, surtout quand on débute. On peut faire des erreurs facilement, comme des oublis de jointures ou des injections SQL si on ne fait pas gaffe. Utiliser un ORM, ça permet de gagner du temps, d’avoir moins de code répétitif, et c’est plus naturel quand on vient du monde objet comme Python. Donc pour éviter le SQL brut, surtout pour des tâches simples, c’est clairement un confort

**2. Que gagne-t-on en utilisant un ORM comme SQLAlchemy ?**

On gagne beaucoup en lisibilité et en maintenance. On peut créer, lire ou modifier des enregistrements sans jamais penser aux requêtes SQL exactes. C’est un gros avantage pour travailler en équipe avec des gens qui ne sont pas à l’aise avec SQL. Et le fait que ça s’intègre bien avec Flask

**3. Est-ce que l’ORM vous empêche complètement d’accéder au SQL si besoin ?**

Non, on peut utiliser les fonctions haut niveau, mais aussi injecter du SQL brut quand on a des besoins spécifiques ou quand c’est plus performant

**4. Est-ce que le code Python devient plus clair ou plus opaque avec un ORM ?**

Je dirais que le code devient plus clair au début, surtout pour les opérations simples. Mais dès qu’on fait des choses un peu complexes (relations entre tables, jointures, etc...), l’abstraction peut cacher des choses importantes, et du coup, faut connaître un minimum ce qui se passe derrière. Donc c’est clair si on comprend bien l’outil, sinon ça peut devenir un peu opaque.

**5. À quel moment l’ORM peut devenir un inconvénient ?**

Pour nous, l’ORM peut poser problème quand on a des besoins très spécifiques en performance, genre des requêtes ultra optimisées ou des traitements de masse. Là, l’ORM peut générer du SQL pas optimal, et c’est mieux de reprendre la main
