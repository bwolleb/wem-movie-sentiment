# MA-WEM: Projet - Analyse de sentiments des films basés sur les dialogues

- Massimo De Santis
- Benoist Wolleb

# Analyse des données
Afin d’explorer les données que nous avons obtenues via le dump Wikipédia ainsi que l’extraction depuis OpenSubtitles, nous travaillons dans des notebooks jupyter, ce qui nous permet une grande flexibilité. Une fois que les différents traitements à apporter aux données ainsi qu’aux résultats, obtenus via les algorithmes ou modèles d’intelligence artificielle, sont connus, le code est nettoyé et placé dans différents scripts python qui peuvent alors être utilisés directement.

Notre cas d’étude est le film “Interstellar” réalisé par Christopher Nolan et sorti en 2014. Nous l’avons sélectionné tout simplement car nous l’avions tous deux vu, car il possède une évolution scénaristique typique (en 3 actes) et est centré sur des thématiques probablement simples à détecter de manière automatique : science-fiction, famille, amour, trahison.

![Interstellar](images/interstellar.jpg)

Les caractéristiques que nous souhaitons extraire de manière automatique sont les suivantes :
- Analyse de sentiments depuis les lignes de dialogue, ce qui ramené à l’échelle du film entier permettrait de déterminer l’évolution dramatique générale tout au long du déroulement du film.
- Extraction des thèmes et mots clés, ce qui permettrait d’isoler les sujets principaux et de classer les films par thème, de manière automatique.
- Calcul de diverses statistiques de langage, comme la richesse du vocabulaire ou l’indice de lisibilité.

## Analyse de sentiments
L’analyse de sentiments des films est au cœur de notre projet. Tout l’enjeu sera de déterminer si les changements d’émotions détectés via les dialogues sont cohérents par rapport à la véritable évolution dramatique du film. En effet, bien que le texte lui-même soit porteur de sens, l’émotion est aussi en très grande partie véhiculée par les acteurs, dans la manière de dire les répliques, ainsi que leur jeu de manière générale, et ce qu’il se passe à l’image bien évidemment.

Notre première intuition a été de grouper les sous-titres, afin d’effectuer l’analyse sur plus d’une seule ligne de dialogue. Le langage “parlé”, contrairement à de la prose littéraire, est relativement peu riche syntaxiquement et il est probable qu’analyser les sentiments d’une seule phrase donne des résultats très pauvres.

Nous avons donc groupé les sous-titres dans une fenêtre temporelle de 15 secondes, obtenant ainsi 4 mesures par minutes, soit 240 par heure, au plus car il y a probablement plusieurs intervalles où, selon l’action à l’écran, aucun dialogue n’est présent. La séparation en petits blocs de quelques secondes permet probablement aussi d’obtenir une mesure cohérente par rapport à la scénographie du film. En effet, la tonalité dramatique est en principe cohérente au sein d’une même scène, mais peut changer radicalement lors d’un changement de scène. Effectuer une mesure sur des intervalles séparés dans le temps permet probablement d’isoler les dialogues par scène.

Ensuite, le texte est passé pour analyse de sentiments au modèle “Twitter-roBERTa-base for Sentiment Analysis” [twitter-roberta-base-sentiment-latest](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) qui est un modèle de type BERT (transformer) entraîné pour la classification en 3 classes “négatif”, “positif” et “neutre” sur des extraits de Twitter. Ce modèle fournit en sortie un score de probabilité entre 0 et 1 pour les 3 classes.

![sentiment_raw](images/sentiment_raw.png)

L’analyse “brute” des sentiments depuis les dialogues est très bruitée, ce qui était attendu car, comme dit plus haut, il est difficile de calculer la tonalité depuis le langage parlé. Sur ces données, nous avons appliqué un lissage par moyennes mouvantes en essayant plusieurs largeurs de fenêtre et avons obtenu des résultats très intéressants, et visuellement interprétables :

![sentiment_mov_avg](images/sentiment_mov_avg.png)

Premièrement, on constate de manière assez logique que les courbes sont inversement corrélées. Deuxièmement, les différents pics semblent marquer la présence de pivots dramatiques, et un dénouement très clairement positif dans les 15 dernières minutes. Nous avons analysé depuis le film lui-même à quoi ces pics correspondent (attention, « divulgâchage » du film ci-après) :
 
![sentiment_interstellar](images/sentiment_interstellar.png)

<table>
	<tr>
	<td><img src="images/interstellar_1.png" alt="1" width = 400px></td>
	<td><p>Premier segment : exposition de la situation de départ. Cette partie est plutôt négative car elle présente un monde hostile et sans espoir, où l’humanité peine à survivre.</p></td>
	</tr>
	<tr>
	<td><img src="images/interstellar_2.png" alt="2" width = 400px></td>
	<td><p>Second segment : cette partie est caractérisée par l’espoir. Une solution pour ”sauver le monde” est présentée au personnage principal.</p></td>
	</tr>
	<tr>
	<td><img src="images/interstellar_3.png" alt="3" width = 400px></td>
	<td><p>Troisième segment : durant cette partie, les personnages explorent la planète Miller qui s’avère inhospitalière et offre l’un des moments les plus stressants du film, accompagné d’une séquence chargée en émotions après l’action principale.</p></td>
	</tr>
	<tr>
	<td><img src="images/interstellar_4.png" alt="4" width = 400px></td>
	<td><p>Quatrième segment : cette longue partie est le pivot dramatique du film, et beaucoup d’éléments en parallèle aggravent l’intrigue : révélations et mort du professeur Brand, trahison du docteur Mann et récupération de la situation par les personnages principaux, non sans dommage. Cette partie est la plus intense et stressante du film.</p></td>
	</tr>
	<tr>
	<td><img src="images/interstellar_5.png" alt="5" width = 400px></td>
	<td><p>Cinquième segment : durant ce dernier acte, la situation se résout pour les personnages, sauvant l’humanité au passage. Le final, bien que chargé en émotions est définitivement positif et porteur d’espoirs.</p></td>
	</tr>
</table>

L’analyse semble ici avoir relativement bien représenté l’évolution dramatique de l’intrigue, avec évidemment quelques imprécisions.

## Caractérisation et similitudes

À partir des données extraites au point précédent, nous nous sommes intéressés à caractériser l’évolution dramatique des films afin de pouvoir retrouver les films les plus similaires, ou du moins possédant une “signature” émotionnelle semblable.
Nous avons commencé par ajouter une courbe aux données du film, en calculant simplement la différence entre le score positif et négatif sur les courbes lissées :

![diff](images/diff.png)

Cette courbe est moins visuellement interprétable que la visualisation des courbes positive et négative, mais a le mérite de caractériser l’évolution de manière unidimensionnelle.
Ensuite, il nous a semblé hasardeux de comparer l’évolution dramatique des fims directement en utilisant ces données, pour plusieurs raisons :
    • Cette courbe de différence est très bruitée
    • Il y a beaucoup trop de données et comparer les films sur des milliers de mesures n’est probablement pas efficace
    • Les données ne sont pas normalisées, il y aura donc des problèmes en comparant des films de longueur différente.
Nous avons donc décidé de caractériser cette courbe “delta” en effectuant une régression polynomiale tout en normalisant la courbe sur une échelle de 0 à 100. Après quelques essais, le nombre de degrés de la régression a été fixé à 16 (donc 17 facteurs incluant le facteur constant) :

![polyfit](images/polyfit.png)

Nous avons donc maintenant une caractérisation de l’évolution dramatique en 17 facteurs qui représente la “signature” du film. C’est sur cette base que nous allons pouvoir effectuer un calcul de similarité entre les films.

Nous avons tenté de comparer ces signatures directement, en calculant l’erreur quadratique moyenne (MSE) sur les facteurs directement, cependant cette technique ne s’est pas avérée concluante car les valeurs de ceux-ci diffèrent de plusieurs ordres de magnitude :

![match_poly](images/match_poly.png)

Nous avons donc directement calculé l’erreur quadratique moyenne sur les valeurs des courbes entre 0 et 100 et avons obtenu un résultat beaucoup plus pertinent :

![match_curve](images/match_curve.png)

Il est cependant à noter que rien ne garantit qu’une signature dramatique similaire permette de retrouver des films similaires dans leurs thématiques, car il ne s’agit que de l’évolution de la tonalité dramatique. Ces données devront donc être couplés avec la partie suivante qui s’occupe d’extraire les thèmes à partir des dialogues afin de retrouver des films réellement semblables, tant dans leurs thématiques que dans leur déroulement.

## Extraction des thèmes
Les catégories dans lesquelles les films sont répertoriés n’ont parfois que peu de sens. En effet, un film ayant un scénario complexe, qui mélange une multitude de thèmes et d’enjeux sera probablement répertorié dans une catégorie “fourre-tout” comme “action” ou “drame”.

Pour illustrer cet effet, on peut par exemple citer le film “Cloud Atlas” réalisé par Tom Tykwer ainsi que les sœurs Wachowski, sorti en 2012. Ce film raconte six histoires en parallèle, se déroulant à plusieurs époques différentes et avec des thèmes très variés.

![cloud_atlas](images/cloud_atlas.jpg)

De tous ces segments, seulement deux se déroulent dans le futur et pourtant le film est identifié dans les catégories ”science-fiction”, ”drame” et ”mystère” ([IMDB](https://www.imdb.com/title/tt1371111)).

En effectuant une extraction des thèmes directement depuis les dialogues du film, nous espérons obtenir un résultat plus précis, ou du moins plus pertinent des véritables thématiques abordées par le scénario et les personnages.

Le modèle que nous utilisons pour cette tâche est [bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli) entraîné par Facebook et qui permet d'effectuer une "Zero Shot Text Classification". Concrètement, le modèle prend un texte à évaluer et une liste de tags en entrée, et fournit les probabilités associées pour chacun de ces tags en sortie.

Nous avons donc établi une liste de 100 tags à associer aux films qui vont de valeurs très génériques comme "action", "adventure", "thriller" à des valeurs un peu plus spécifiques comme "coming of age", "journey" ou "dark comedy".

Pour cette analyse, nous ne procédons plus ligne par ligne, mais en concaténant les dialogues du film entier en une seul chaîne qui est transmise au modèle, car la pipeline fournie par HuggingFace supporte les longues chaînes en entrée.

Enfin, à partie de la sortie du modèle, nous associons les tags ayant les plus grandes probabilités, tout d'abord en prenant les 3 plus grandes (afin de systématiquement avoir 3 valeurs pour chaque film, même si les probabilités sont faibles) puis en sélectionnant les éventuelles suivantes si elles dépassent un certain seuil. Sur les 9170 films de notre sélection, nous obtenons ainsi la distribution suivante:

![tags_per_movie](images/tags_per_movie.png)

En examinant la distribution par tag pour les 25% les plus fréquents, celle-ci est, comme on pouvait s'y attendre, assez inégale:

![tags_dist](images/tags_dist.png)

Sans surprise, ce sont les tags les plus génériques qui sont les plus fréquemments associés, alors que les tags plus spécifiques le sont beaucoup plus rarement (75 valeurs très petites ne sont pas affichées).

Maintenant, en examinant la pertinence de ceux-ci, nous nous sommes aperçus que, contrairement à ce que nous espérions, la détection des ces tags n'est fréquemment pas très juste. Pour reprendre notre cas d'étude ainsi que l'exemple ci-dessus, nous obtenons les données suivantes:

- Interstellar: business, action, journey
- Cloud Atlas: future, journey, computer

S'agissant d'Interstellar, le tag "journey", et dans une moindre mesure le tag "action", sont plutôt pertinents. Cependant, ous somme surpris d'y retrouver le tag "business" qui semble assez hors contexte. Connaissant le film et son sujet, nous aurions préféré retrouver les tags "sci-fi", "space", "drama", "family" et éventuellement "post-apocalyptic" et "love" alors que ceux-ci n'ont pas été jugés pertinents par le modèle, les classant respectivement en positions 68, 22, 21, 33, 49 et 84 (et avec des scores très bas).

Pour le second cas, les tags obtenus sont plutôt cohérents. S'agissant comme expliqué d'un film racontant plusieurs segments très éloignés les uns des autres, sans thème central apparent, le tag "journey" semble un bon indicateur, et les tags "future" et "computer" ont probablement été détectés sur les segments les plus futuristes, lesquels utilisent peut-être un vocabulaire plus "typé" et reconnaissable que les autres.

Enfin, pour plusieurs de films, les tags sont parfois extrêmements contre-intuitifs, en particulier pour les films d'horreur qui semblent être particulièrement mal catégorisés. Par exemple, le film Saw est catégorisé en "future", "action" et "journey".

Notre hypothèse pour expliquer ceci est probablement que le modèle ne reconnaît pas aussi facilement certains thèmes, potentiellement plus rares et associés à moins de "mots clés" ou "mots déclencheurs" que certains autres un peu plus génériques, ce qui est typiquement visible dans le graphique ci-dessus.

Par exemple, il y a probablement beaucoup de mots ou de phrases qui sont habituellement corrélées à de l'action, et relativement peu au genre du film noir, qui est une catégorisation plutôt visuelle que narrative. Le thèmes sous-jacents au texte fourni au modèle sont probablement aussi très "dilués", car beaucoup de lignes de dialogue sont probablement peu eplicatives et pauvres de sens, une caractéristique typique du langage parlé. 

Il faudrait donc que le modèle ait une très grande sensibilité associées à chaque tag pour pouvoir correctement les détecter, ce qui n'est clairement pas le cas des modèles de type "Zero Shot Classification" et nécessiterait un peu de *fine-tuning*.

Pour pallier à ce problème, une idée d'amélioration serait par exemple de faire l'analyse en plusieurs passes: la première en ne fournissant qu'une dizaine de tags très génériques, permettant de catégoriser grossièrement le type de film, et une seconde phase en fournissant un sous-ensemble de tags associés à la catégorie plus générique détectée à la première phase. Par exemple la catégorie large "suspense" pourrait être associée à des sous-catégies comme "conspiracy", "crime", "detective", "murder", "spy" etc.

Il serait aussi possible de "nettoyer" un peu plus le texte fourni au modèle, par exemple en supprimant complètement les mots ou même des phrases entières jugées comme pauvres en sens.

## Limites
Films avec peu de dialogue
Erreurs dans les fichiers lors de la collecte
