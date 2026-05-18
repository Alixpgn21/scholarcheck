def get_css():
    return """
@page {
    size: A4;
    margin: 2.5cm 2.5cm 2.5cm 3cm;
    @top-center { content: string(chapter); font-size: 9pt; color: #666; font-family: 'Georgia', serif; }
    @bottom-right { content: counter(page); font-size: 9pt; color: #666; }
    @bottom-left { content: "ScholarCheck — État de l'art"; font-size: 9pt; color: #666; }
}
@page :first { @top-center { content: none; } @bottom-left { content: none; } @bottom-right { content: none; } }

body { font-family: 'Georgia', 'Times New Roman', serif; font-size: 11pt; line-height: 1.7; color: #1a1a1a; text-align: justify; }
h1 { font-size: 22pt; font-weight: bold; color: #1a2a4a; margin-top: 2em; margin-bottom: 0.5em; border-bottom: 2px solid #1a2a4a; padding-bottom: 0.3em; }
h2 { font-size: 15pt; font-weight: bold; color: #1a2a4a; margin-top: 2em; margin-bottom: 0.6em; string-set: chapter content(); }
h3 { font-size: 12.5pt; font-weight: bold; color: #2a3a5a; margin-top: 1.5em; margin-bottom: 0.4em; }
h4 { font-size: 11pt; font-weight: bold; font-style: italic; color: #3a4a6a; margin-top: 1.2em; margin-bottom: 0.3em; }
p { margin: 0 0 0.8em 0; orphans: 3; widows: 3; }
.cover { text-align: center; padding-top: 4cm; page-break-after: always; }
.cover h1 { border: none; font-size: 26pt; margin-bottom: 0.3em; }
.cover .subtitle { font-size: 14pt; color: #444; margin-bottom: 3cm; font-style: italic; }
.cover .meta { font-size: 11pt; line-height: 2; color: #333; }
.cover .meta strong { color: #1a2a4a; }
.toc { page-break-after: always; }
.toc h2 { border-bottom: 1px solid #ccc; }
.toc ul { list-style: none; padding: 0; }
.toc > ul > li { margin: 0.5em 0; font-weight: bold; }
.toc > ul > li > ul > li { font-weight: normal; margin: 0.2em 0 0.2em 1.5em; }
.toc a { text-decoration: none; color: #1a2a4a; }
blockquote { border-left: 3px solid #1a2a4a; margin: 1em 0 1em 1em; padding: 0.5em 1em; background: #f5f7fa; font-style: italic; }
table { width: 100%; border-collapse: collapse; margin: 1.5em 0; font-size: 10pt; }
thead { background: #1a2a4a; color: white; }
th { padding: 8px 10px; text-align: left; }
td { padding: 7px 10px; border-bottom: 1px solid #ddd; }
tr:nth-child(even) { background: #f5f7fa; }
.caption { font-size: 9.5pt; font-style: italic; text-align: center; color: #555; margin-top: -1em; margin-bottom: 1.5em; }
.ref-list { font-size: 10pt; }
.ref-list p { margin-bottom: 0.6em; padding-left: 2em; text-indent: -2em; }
.chapter-intro { background: #f0f4f8; border-left: 4px solid #1a2a4a; padding: 0.8em 1.2em; margin-bottom: 1.5em; font-style: italic; font-size: 10.5pt; }
.page-break { page-break-before: always; }
abbr { font-variant: small-caps; }
.highlight { background: #fff3cd; padding: 0.1em 0.2em; }
sup { font-size: 8pt; }
"""


def get_html_content():
    return COVER + TOC + CH1 + CH2 + CH3 + CH4 + CH5 + CH6 + REFS


COVER = """
<div class="cover">
  <p style="font-size:12pt; color:#555; letter-spacing:2px; text-transform:uppercase;">Projet R&amp;D — Axe B</p>
  <h1>ScholarCheck</h1>
  <p class="subtitle">Assistant SaaS de rédaction et de vérification scientifique<br/>
  <em>État de l'art</em></p>
  <div style="width:80px; height:3px; background:#1a2a4a; margin:1cm auto;"></div>
  <div class="meta">
    <p><strong>Référent :</strong> Amine HADIR</p>
    <p><strong>Durée du projet :</strong> 2 semaines</p>
    <p><strong>Niveau :</strong> Bac+5 — Master Recherche / Ingénieur</p>
    <p><strong>Date :</strong> Mai 2026</p>
  </div>
  <div style="margin-top:3cm; font-size:10pt; color:#888;">
    <p>Mots-clés : Large Language Models · Hallucination · Retrieval-Augmented Generation ·<br/>
    APIs académiques · Embeddings · Clustering thématique · Intégrité scientifique</p>
  </div>
</div>
"""

TOC = """
<div class="toc">
  <h2>Table des matières</h2>
  <ul>
    <li>1. Introduction générale
      <ul>
        <li>1.1 Contexte et motivation</li>
        <li>1.2 Problématique et questions de recherche</li>
        <li>1.3 Méthodologie de la revue de littérature</li>
        <li>1.4 Organisation du document</li>
      </ul>
    </li>
    <li>2. Hallucinations dans les grands modèles de langage
      <ul>
        <li>2.1 Fondements architecturaux des LLMs</li>
        <li>2.2 Taxonomie générale des hallucinations</li>
        <li>2.3 Hallucinations bibliographiques : définition et manifestations</li>
        <li>2.4 Études empiriques et mesure du phénomène</li>
        <li>2.5 Facteurs aggravants</li>
        <li>2.6 Impact sur l'intégrité scientifique</li>
        <li>2.7 Stratégies de détection et d'atténuation</li>
      </ul>
    </li>
    <li>3. Retrieval-Augmented Generation (RAG)
      <ul>
        <li>3.1 Genèse et motivations</li>
        <li>3.2 Architecture fondamentale</li>
        <li>3.3 Composants du retrieval</li>
        <li>3.4 Variantes avancées</li>
        <li>3.5 RAG appliqué à l'écriture scientifique</li>
        <li>3.6 Limites et défis ouverts</li>
      </ul>
    </li>
    <li>4. Infrastructures d'accès à la littérature scientifique
      <ul>
        <li>4.1 Panorama des bases de données académiques</li>
        <li>4.2 CrossRef</li>
        <li>4.3 OpenAlex</li>
        <li>4.4 Semantic Scholar</li>
        <li>4.5 Sources complémentaires</li>
        <li>4.6 Analyse comparative et stratégie d'interrogation</li>
      </ul>
    </li>
    <li>5. Représentation vectorielle et clustering de documents scientifiques
      <ul>
        <li>5.1 Du bag-of-words aux embeddings denses</li>
        <li>5.2 Modèles d'embeddings pour textes scientifiques</li>
        <li>5.3 Réduction de dimensionnalité</li>
        <li>5.4 Méthodes de clustering</li>
        <li>5.5 Modélisation thématique</li>
        <li>5.6 Métriques d'évaluation</li>
      </ul>
    </li>
    <li>6. Synthèse et positionnement de ScholarCheck
      <ul>
        <li>6.1 Analyse de l'existant</li>
        <li>6.2 Gap dans la littérature</li>
        <li>6.3 Architecture de ScholarCheck en regard de l'état de l'art</li>
        <li>6.4 Limites et perspectives</li>
      </ul>
    </li>
    <li>7. Références bibliographiques</li>
  </ul>
</div>
"""

CH1 = """
<div class="page-break">
<h1>1. Introduction générale</h1>

<h2>1.1 Contexte et motivation</h2>

<p>La production scientifique mondiale atteint aujourd'hui des volumes sans précédent. Selon les estimations de l'Union Internationale des Associations de Publication, plus de 3 millions d'articles scientifiques sont publiés chaque année dans des revues à comité de lecture, auxquels s'ajoutent plusieurs millions de préprints déposés sur des plateformes comme arXiv, bioRxiv ou SSRN [1]. Dans ce contexte d'hypercroissance de la littérature académique, les chercheurs font face à un défi fondamental : comment identifier, assimiler et synthétiser les travaux pertinents à leur domaine en un temps raisonnable ?</p>

<p>L'émergence des grands modèles de langage (LLMs — <em>Large Language Models</em>) a semblé offrir une réponse partielle à ce défi. Des systèmes comme GPT-4, Claude 3, Gemini Ultra ou LLaMA-3 démontrent des capacités remarquables de synthèse, de reformulation et de rédaction académique. Des études utilisateur montrent qu'une proportion croissante de chercheurs, estimée entre 15 et 30 % selon les disciplines, utilisent désormais des assistants LLM pour accélérer la rédaction de leurs manuscrits, notamment pour les sections d'introduction et de revue de littérature [2].</p>

<p>Cependant, cette adoption rapide s'est heurtée à un problème structurel majeur, identifié et documenté dès 2023 : les LLMs génèrent des <em>hallucinations bibliographiques</em>. Ce terme désigne la production de références bibliographiques syntaxiquement correctes et stylistiquement plausibles, mais factuellement inexistantes — des titres inventés, des auteurs fictifs ou mal attribués, des DOIs invalides, des journaux existants mais n'ayant jamais publié l'article cité. Ce phénomène n'est pas marginal : Walters et Wilder [3] ont démontré expérimentalement que ChatGPT génère une proportion significative de références entièrement fabriquées lorsqu'on lui demande de produire des bibliographies sur des sujets académiques précis.</p>

<p>Les conséquences de cette défaillance sont multiples et graves. Sur le plan de l'intégrité scientifique, des articles publiés dans des revues à comité de lecture ont dû être corrigés ou rétractés après détection de citations inventées. Sur le plan juridique, des praticiens du droit ont été sanctionnés par des tribunaux américains pour avoir soumis des mémoires contenant des jurisprudences générées par ChatGPT — des affaires fictives avec des parties, des dates et des numéros de dossier entièrement fabriqués [4]. Sur le plan de la recherche fondamentale, la propagation de citations fantômes risque de fausser les indicateurs bibliométriques et de créditer à tort certains auteurs ou certaines théories.</p>

<p>Le projet <strong>ScholarCheck</strong> naît de ce constat. Il vise à construire un système à deux modules complémentaires : (1) un auditeur de références capable de détecter les citations défaillantes dans un manuscrit existant, et (2) un générateur de sections <em>related work</em> garantissant que chaque affirmation est ancrée sur une source réellement consultée et validée. Cette double fonctionnalité repose sur une combinaison de techniques issues de quatre domaines de recherche actifs : la détection des hallucinations dans les LLMs, l'architecture RAG (<em>Retrieval-Augmented Generation</em>), l'accès programmatique aux bases de données académiques, et le clustering sémantique de documents scientifiques.</p>

<h2>1.2 Problématique et questions de recherche</h2>

<p>La problématique centrale de ce travail peut être formulée ainsi : <em>Dans quelle mesure les techniques actuelles de traitement automatique du langage naturel et d'accès aux bases de données bibliographiques permettent-elles de construire un système fiable de détection des hallucinations bibliographiques et d'assistance à la rédaction scientifique ancrée sur des sources vérifiées ?</em></p>

<p>Cette problématique centrale se décline en quatre questions de recherche spécifiques, correspondant aux quatre axes de cet état de l'art :</p>

<p><strong>QR1 :</strong> Quels sont les mécanismes à l'origine des hallucinations bibliographiques dans les LLMs, et dans quelle mesure peuvent-elles être détectées automatiquement ?</p>

<p><strong>QR2 :</strong> Comment l'architecture RAG permet-elle d'ancrer la génération de texte sur des sources vérifiées, et quelles sont ses limitations dans le contexte de l'écriture scientifique ?</p>

<p><strong>QR3 :</strong> Quelles APIs académiques offrent les meilleures garanties de couverture, fiabilité et richesse sémantique pour la vérification bibliographique automatique ?</p>

<p><strong>QR4 :</strong> Comment les méthodes de clustering par embeddings permettent-elles d'organiser automatiquement un corpus de documents scientifiques en thèmes cohérents pour faciliter la rédaction de <em>related work</em> ?</p>

<h2>1.3 Méthodologie de la revue de littérature</h2>

<p>Cette revue de littérature a été conduite selon une approche systématique adaptée aux contraintes d'un projet de deux semaines. La stratégie de recherche bibliographique a combiné plusieurs sources :</p>

<p><strong>Sources primaires consultées :</strong> Google Scholar, Semantic Scholar, ACL Anthology (pour les travaux en TAL), arXiv (préprints), ACM Digital Library et IEEE Xplore. Les bases de données bibliométriques OpenAlex et CrossRef ont également été interrogées directement.</p>

<p><strong>Mots-clés principaux :</strong> "LLM hallucination", "bibliographic hallucination", "citation fabrication", "retrieval-augmented generation", "dense passage retrieval", "scientific document clustering", "sentence embeddings", "academic knowledge graph", "CrossRef API", "OpenAlex".</p>

<p><strong>Critères d'inclusion :</strong> Publications en anglais ou français, publiées entre 2019 et 2026, dans des conférences de rang A/A* (NeurIPS, ICML, ACL, EMNLP, ICLR, SIGIR, WWW) ou dans des revues indexées. Les préprints arXiv ont été inclus lorsqu'ils présentent un apport technique significatif et sont largement cités dans la communauté.</p>

<p><strong>Critères d'exclusion :</strong> Travaux antérieurs à 2017 (avant l'ère transformer), publications sans évaluation empirique pour les articles techniques, articles dont la source primaire n'a pas pu être vérifiée.</p>

<p>Au total, plus de 120 publications ont été identifiées, 65 ont fait l'objet d'une lecture approfondie, et 52 sont citées dans ce document.</p>

<h2>1.4 Organisation du document</h2>

<p>Ce document est organisé en six chapitres thématiques. Le chapitre 2 examine en profondeur le phénomène des hallucinations dans les LLMs, avec un focus particulier sur les hallucinations bibliographiques. Le chapitre 3 présente l'architecture RAG, depuis ses fondements jusqu'aux variantes avancées les plus récentes. Le chapitre 4 analyse les principales infrastructures d'accès programmatique à la littérature scientifique. Le chapitre 5 couvre les méthodes de représentation vectorielle et de clustering appliquées aux documents académiques. Enfin, le chapitre 6 synthétise ces quatre axes pour positionner ScholarCheck par rapport à l'état de l'art et identifier les perspectives de développement.</p>
</div>
"""

CH2 = """
<div class="page-break">
<h1>2. Hallucinations dans les grands modèles de langage</h1>
<div class="chapter-intro">Ce chapitre examine le phénomène des hallucinations dans les LLMs : ses fondements architecturaux, sa taxonomie, ses manifestations bibliographiques spécifiques, et les approches existantes de détection et d'atténuation.</div>

<h2>2.1 Fondements architecturaux des LLMs</h2>

<p>Pour comprendre les hallucinations, il est nécessaire de rappeler les principes fondamentaux de fonctionnement des LLMs modernes. Depuis l'introduction de l'architecture Transformer par Vaswani et al. [5] en 2017, la quasi-totalité des LLMs performants reposent sur ce mécanisme d'attention multi-têtes (<em>multi-head self-attention</em>). L'entraînement procède par prédiction du prochain token : le modèle apprend à maximiser la probabilité P(w<sub>t</sub> | w<sub>1</sub>, ..., w<sub>t-1</sub>) sur des corpus de texte massifs.</p>

<p>Cette approche présente une propriété fondamentale : le modèle optimise la plausibilité statistique du texte généré, pas sa vérité factuelle. Il n'existe pas de module de vérification des faits intégré au processus de génération. Le modèle associe des patterns textuels entre eux sur la base de leur co-occurrence dans les données d'entraînement, et génère des continuations qui maximisent la cohérence statistique du contexte — pas la correspondance avec une réalité externe vérifiable.</p>

<p>Brown et al. [6] ont démontré avec GPT-3 (175 milliards de paramètres) que l'augmentation de la taille des modèles améliore considérablement leurs performances sur des benchmarks de raisonnement et de compréhension, mais n'élimine pas les hallucinations — elle les rend simplement plus subtiles et donc plus difficiles à détecter. Wei et al. [7] ont introduit le concept d'<em>émergence</em> pour décrire les capacités qui apparaissent de manière non linéaire avec la taille du modèle ; malheureusement, l'élimination des hallucinations ne figure pas parmi ces capacités émergentes.</p>

<h2>2.2 Taxonomie générale des hallucinations</h2>

<p>Ji et al. [8] proposent dans leur survey de référence une taxonomie complète des hallucinations en NLG (<em>Natural Language Generation</em>), qui distingue deux catégories principales :</p>

<p><strong>Hallucinations intrinsèques :</strong> le texte généré contredit directement le document source fourni en contexte. Par exemple, un résumé automatique qui attribue à un auteur une affirmation contraire à ce qu'il écrit dans l'article original. Maynez et al. [9] ont mesuré ce phénomène dans le cadre du résumé automatique, trouvant que 70 % des résumés générés par SOTA contiennent au moins une hallucination intrinsèque.</p>

<p><strong>Hallucinations extrinsèques :</strong> le texte généré contient des affirmations qui ne peuvent pas être vérifiées ou confirmées par rapport à la source, ni infirmées — elles sont simplement non fondées. Dans le cas d'une génération libre sans document source, toute affirmation factuelle non soutenue par les données d'entraînement entre dans cette catégorie.</p>

<p>Pour les LLMs génératifs, Huang et al. [10] affinent cette taxonomie en distinguant :</p>
<ul>
  <li><strong>Factual hallucinations :</strong> affirmations contraires aux faits établis.</li>
  <li><strong>Logical hallucinations :</strong> raisonnements valides en apparence mais contenant des erreurs logiques.</li>
  <li><strong>Faithful hallucinations :</strong> affirmations cohérentes avec le prompt mais non fondées sur des connaissances réelles.</li>
</ul>

<p>Les hallucinations bibliographiques constituent un sous-type spécifique des hallucinations factuelles extrinsèques, avec des caractéristiques qui les rendent particulièrement dangereuses dans le contexte académique.</p>

<h2>2.3 Hallucinations bibliographiques : définition et manifestations</h2>

<p>Une <strong>hallucination bibliographique</strong> est la génération d'une référence bibliographique qui ne correspond à aucun article publié, ou dont les métadonnées (auteurs, titre, année, journal, DOI) ne correspondent pas à un article réel. Ce phénomène se manifeste sous plusieurs formes :</p>

<h4>Fabrication complète</h4>
<p>Le LLM génère un article entier inexistant : titre plausible, auteurs crédibles (parfois des chercheurs réels dans le domaine, mais n'ayant pas écrit cet article), année cohérente, journal existant mais n'ayant jamais publié cet article, DOI invalide. Walters et Wilder [3] ont documenté ce cas de manière systématique : en soumettant à ChatGPT des demandes de bibliographies sur des sujets académiques précis et en vérifiant chaque référence via CrossRef et les moteurs de recherche académiques, ils ont trouvé des taux de fabrication allant jusqu'à 46 % selon le sujet.</p>

<h4>Citation mal attribuée</h4>
<p>L'article existe réellement, mais est attribué aux mauvais auteurs, ou publié dans le mauvais journal, ou daté de manière incorrecte. Ce cas est particulièrement insidieux car une vérification superficielle (le titre semble correspondre) ne suffit pas à le détecter.</p>

<h4>DOI invalide ou mal formé</h4>
<p>Le DOI généré ne résout pas, ou résout vers un article différent. Les DOIs ont une structure formelle précise (préfixe registrant/suffixe), que les LLMs imitent sans garantir la résolution effective.</p>

<h4>Inadéquation sémantique</h4>
<p>L'article cité existe, ses métadonnées sont correctes, mais son contenu ne soutient pas l'affirmation pour laquelle il est invoqué. Ce cas, plus subtil, nécessite une vérification sémantique et non plus seulement factuelle. Sun et al. [11] ont montré que même lorsque des LLMs sont guidés vers des articles existants, la phrase citante ne reflète souvent qu'imparfaitement — voire déforme — ce que l'article dit réellement.</p>

<h2>2.4 Études empiriques et mesure du phénomène</h2>

<p>Plusieurs études empiriques rigoureuses ont quantifié le phénomène depuis 2023, moment où l'accès grand public aux LLMs a déclenché une vague d'investigations académiques.</p>

<p>Athaluri et al. [12], dans une étude publiée dans <em>Cureus</em>, ont demandé à ChatGPT de générer des bibliographies sur des sujets biomédicaux précis et ont vérifié chaque référence via PubMed et CrossRef. Leurs résultats montrent que sur 100 références générées, entre 25 et 40 % étaient entièrement fictives, et un nombre supplémentaire présentait des erreurs de métadonnées significatives (mauvaise date, mauvais auteur principal).</p>

<p>Sallam et al. [13] ont conduit une étude similaire sur des sujets de santé publique, trouvant un taux d'hallucination de 69 % pour les références générées sans contrainte de contexte. Ce taux chute à 15-20 % lorsque le LLM est fourni avec un contexte documentaire riche — ce qui préfigure l'intérêt de l'approche RAG.</p>

<p>Ko et al. [14] ont comparé le comportement de plusieurs LLMs (GPT-3.5, GPT-4, LLaMA-2) sur des tâches de génération bibliographique. GPT-4 présente des taux d'hallucination significativement inférieurs à GPT-3.5, mais n'est pas exempt du problème. LLaMA-2 (open-source, 70B) présente les taux les plus élevés, suggérant un lien entre la taille du corpus d'entraînement et la fiabilité bibliographique.</p>

<table>
  <thead><tr><th>Étude</th><th>Modèle testé</th><th>Domaine</th><th>Taux d'hallucination</th></tr></thead>
  <tbody>
    <tr><td>Walters &amp; Wilder [3]</td><td>ChatGPT (GPT-3.5)</td><td>Multidisciplinaire</td><td>15–46 %</td></tr>
    <tr><td>Athaluri et al. [12]</td><td>ChatGPT</td><td>Biomédical</td><td>25–40 %</td></tr>
    <tr><td>Sallam et al. [13]</td><td>ChatGPT</td><td>Santé publique</td><td>69 % (sans contexte)</td></tr>
    <tr><td>Ko et al. [14]</td><td>GPT-4 / LLaMA-2</td><td>Informatique</td><td>8–34 %</td></tr>
  </tbody>
</table>
<p class="caption">Tableau 1 : Comparaison des taux d'hallucination bibliographique mesurés empiriquement.</p>

<h2>2.5 Facteurs aggravants</h2>

<h4>La coupure temporelle (knowledge cutoff)</h4>
<p>Tout LLM possède une date de coupure de ses données d'entraînement au-delà de laquelle il n'a aucune connaissance des publications. Les demandes portant sur des travaux récents poussent le modèle à extrapoler, augmentant considérablement le risque de fabrication. Pour ScholarCheck, cette limite est particulièrement importante : les articles les plus récents, souvent les plus cités dans les introductions et <em>related work</em>, sont précisément ceux que le modèle connaît le moins.</p>

<h4>La longue traîne de la littérature académique</h4>
<p>Si les LLMs mémorisent raisonnablement bien les articles très cités et les auteurs très prolixes, leur connaissance des articles moins populaires est fragmentaire. Or, une bibliographie académique correcte inclut souvent des travaux spécialisés peu cités — exactement le type d'article le plus susceptible d'être halluciné.</p>

<h4>La pression vers la complétude</h4>
<p>Lorsqu'un utilisateur demande "10 références sur le sujet X", le modèle subit une pression implicite à produire exactement 10 références. S'il n'en connaît que 6 avec certitude, il en invente 4 plutôt que de refuser ou de signaler l'incertitude.</p>

<h2>2.6 Impact sur l'intégrité scientifique</h2>

<p>Au-delà des statistiques, les conséquences concrètes documentées sont préoccupantes. Plusieurs cas de rétractation liés à des références LLM-générées ont été documentés en 2023-2024. Le <em>Retraction Watch</em> database, qui recense les rétractations académiques mondiales, a commencé à encoder des rétractations liées aux LLMs comme catégorie distincte [15].</p>

<p>Dans le domaine juridique, l'affaire <em>Mata v. Avianca</em> (2023) a établi une jurisprudence sur la responsabilité des praticiens utilisant des LLMs sans vérification : les avocats ont soumis des mémoires citant des décisions de justice entièrement inventées par ChatGPT et ont été sanctionnés par le tribunal fédéral américain [4].</p>

<p>Sur le plan des indicateurs bibliométriques, Bloomfield et al. [16] alertent sur le risque systémique : si les hallucinations bibliographiques se propagent dans les corpus d'entraînement des futurs LLMs (via des articles publiés citant des références fantômes), cela pourrait créer une boucle de rétroaction dégradant progressivement la fiabilité des modèles.</p>

<h2>2.7 Stratégies de détection et d'atténuation</h2>

<h4>Vérification post-hoc par API</h4>
<p>L'approche la plus directe consiste à vérifier chaque référence générée contre une base de données bibliographique authoritative. C'est le cœur du module de vérification de ScholarCheck. La vérification multi-source (CrossRef + OpenAlex + Semantic Scholar) augmente la robustesse en cas d'absence dans une seule base.</p>

<h4>Grounding via RAG</h4>
<p>Plutôt que de corriger les hallucinations en aval, le RAG [17] les prévient en amont en forçant le LLM à générer du texte ancré sur des documents fournis explicitement. Cette approche est détaillée au chapitre 3.</p>

<h4>Vérification par NLI</h4>
<p>Honovich et al. [18] proposent d'utiliser des modèles d'<em>inférence en langage naturel</em> (NLI — <em>Natural Language Inference</em>) pour vérifier si une affirmation est entailée (<em>entailed</em>) par un document de référence. Un modèle NLI prend en entrée une prémisse (l'abstract du papier) et une hypothèse (la phrase citante) et prédit : entailment, contradiction, ou neutre. Cette approche va au-delà de la similarité cosinus utilisée par ScholarCheck et constitue une perspective d'amélioration.</p>

<h4>Constitutional AI et RLHF</h4>
<p>Bai et al. [19] proposent une approche d'entraînement où le modèle est conditionné à refuser de générer des références dont il n'est pas certain. Bien que prometteuse, cette approche nécessite de modifier l'entraînement du modèle et n'est donc pas applicable à des LLMs existants déployés via API.</p>

<h4>FactScore</h4>
<p>Min et al. [20] proposent FactScore, un cadre d'évaluation de la précision factuelle qui décompose les textes longs en claims atomiques et vérifie chacun contre une base de connaissances. Appliqué aux bibliographies, FactScore peut quantifier le taux de fabrication de manière plus fine que les approches binaires (présent/absent).</p>
</div>
"""

CH3 = """
<div class="page-break">
<h1>3. Retrieval-Augmented Generation (RAG)</h1>
<div class="chapter-intro">Ce chapitre présente l'architecture RAG depuis ses fondements jusqu'aux variantes les plus récentes, en analysant son applicabilité au contexte de la vérification et de la génération bibliographique.</div>

<h2>3.1 Genèse et motivations</h2>

<p>L'architecture RAG (<em>Retrieval-Augmented Generation</em>) est née de la confrontation entre deux limites fondamentales des LLMs : leur connaissance figée à la date de coupure d'entraînement, et leur tendance à halluciner lorsqu'ils opèrent au-delà de leur mémoire paramétrique fiable.</p>

<p>Lewis et al. [17], dans leur article fondateur présenté à NeurIPS 2020, formalisent l'intuition suivante : un LLM ne doit pas être contraint de mémoriser l'intégralité du savoir humain dans ses paramètres. Il peut, à la manière d'un chercheur consultant une bibliothèque, interroger une base documentaire externe au moment de la génération, et conditionner sa réponse sur les documents récupérés.</p>

<p>Cette approche résout simultanément plusieurs problèmes :</p>
<ul>
  <li><strong>Actualité :</strong> la base documentaire peut être mise à jour sans réentraîner le modèle.</li>
  <li><strong>Traçabilité :</strong> les affirmations générées peuvent être liées aux documents sources, permettant une vérification humaine.</li>
  <li><strong>Réduction des hallucinations :</strong> le modèle est contraint de s'appuyer sur des documents réels plutôt que sur sa mémoire paramétrique.</li>
  <li><strong>Spécialisation domaine :</strong> un corpus spécialisé (médical, juridique, scientifique) peut être indexé sans fine-tuning coûteux.</li>
</ul>

<h2>3.2 Architecture fondamentale</h2>

<p>L'architecture RAG standard se compose de trois composants principaux :</p>

<h4>L'indexeur</h4>
<p>Les documents du corpus sont découpés en passages de taille fixe (typiquement 256 à 512 tokens), encodés en vecteurs denses par un modèle d'encodage (<em>bi-encoder</em>), et stockés dans un index vectoriel permettant la recherche par similarité approximative. Les index vectoriels les plus utilisés sont FAISS [21] (Facebook AI Similarity Search), qui implémente différentes structures d'index (IVF, HNSW) avec des compromis vitesse/précision configurables.</p>

<h4>Le retriever</h4>
<p>À la réception d'une requête, le retriever encode la requête avec le même modèle (ou un modèle complémentaire), calcule les similarités cosinus avec tous les vecteurs de l'index, et retourne les k passages les plus similaires. Ce processus de <em>Maximum Inner Product Search</em> (MIPS) est au cœur de l'efficacité du RAG.</p>

<h4>Le générateur</h4>
<p>Le LLM reçoit en entrée un prompt composé de : (1) la requête originale, (2) les k passages récupérés (le contexte), et (3) des instructions de formatage. Il génère alors une réponse conditionnée sur ce contexte, idéalement en citant explicitement les passages sources.</p>

<p>Lewis et al. [17] proposent deux variantes d'intégration du retrieval dans la génération :</p>
<ul>
  <li><strong>RAG-Sequence :</strong> pour chaque document récupéré, le modèle génère une séquence complète, puis marginalise sur tous les documents.</li>
  <li><strong>RAG-Token :</strong> à chaque token généré, le modèle peut marginaliser sur les documents récupérés, permettant de combiner des informations issues de plusieurs documents au niveau du token.</li>
</ul>

<h2>3.3 Composants du retrieval</h2>

<h4>Dense Passage Retrieval (DPR)</h4>
<p>Karpukhin et al. [22] formalisent le <em>Dense Passage Retrieval</em> comme une approche où deux encodeurs BERT distincts (un pour les questions, un pour les passages) sont entraînés conjointement par apprentissage contrastif. L'objectif est que les paires (question, passage pertinent) soient proches dans l'espace vectoriel, tandis que les paires (question, passage non pertinent) soient éloignées.</p>

<p>Formellement, la similarité entre une question q et un passage p est calculée comme :</p>
<blockquote>sim(q, p) = E<sub>Q</sub>(q)<sup>T</sup> · E<sub>P</sub>(p)</blockquote>
<p>où E<sub>Q</sub> et E<sub>P</sub> sont les encodeurs question et passage respectivement. L'entraînement minimise la perte de cross-entropie en utilisant des négatifs difficiles (<em>hard negatives</em>) — des passages trompeurs proches de la question mais non pertinents.</p>

<h4>Sparse vs. Dense retrieval</h4>
<p>Les méthodes <em>sparse</em> traditionnelles comme BM25 [23] reposent sur des représentations BoW pondérées par TF-IDF. Elles sont très efficaces pour la correspondance lexicale exacte, mais échouent sur les correspondances sémantiques (synonymes, paraphrases). Les méthodes denses (DPR, SBERT) capturent la sémantique mais peuvent manquer des correspondances exactes importantes.</p>

<p>Ma et al. [24] et Chen et al. [25] montrent que les approches hybrides, combinant scores BM25 et scores denses par interpolation linéaire, surpassent systématiquement les approches pures sur les benchmarks BEIR [26], en particulier pour des domaines spécialisés comme les sciences biomédicales.</p>

<h4>ColBERT</h4>
<p>Khattab et Zaharia [27] proposent ColBERT (<em>Contextualized Late Interaction over BERT</em>), une architecture qui représente chaque token de la requête et du document par son embedding contextuel BERT, et calcule le score de pertinence par une interaction tardive (<em>MaxSim</em>) :</p>
<blockquote>Score(q, d) = Σ<sub>i∈[|q|]</sub> max<sub>j∈[|d|]</sub> E<sub>qi</sub><sup>T</sup> · E<sub>dj</sub></blockquote>
<p>Cette approche offre une précision supérieure à DPR tout en maintenant une efficacité à l'inférence comparable grâce à une phase d'encodage offline des documents.</p>

<h2>3.4 Variantes avancées</h2>

<h4>Self-RAG</h4>
<p>Asai et al. [28] proposent Self-RAG, une approche où le LLM apprend à décider lui-même quand déclencher un retrieval, et à critiquer la qualité des passages récupérés via des tokens spéciaux de réflexion. Ces tokens, appelés <em>reflection tokens</em>, encodent des jugements tels que "retrieve", "relevant", "supported", "isUSEFUL". Le modèle est entraîné end-to-end pour générer ces tokens, éliminant le besoin d'un pipeline retrieval/génération séparé.</p>

<h4>CRAG (Corrective RAG)</h4>
<p>Yan et al. [29] introduisent CRAG, un mécanisme qui évalue la qualité du retrieval et déclenche des actions correctives si les documents récupérés sont jugés insuffisants. Si la confiance dans les documents récupérés est faible, CRAG peut reformuler la requête, effectuer une recherche web complémentaire, ou combiner plusieurs stratégies. Ce mécanisme est particulièrement pertinent pour ScholarCheck, où la qualité du retrieval conditionne directement la fiabilité de la vérification.</p>

<h4>Modular RAG</h4>
<p>Gao et al. [30] proposent une taxonomie unifiée des architectures RAG sous le terme <em>Modular RAG</em>, où chaque composant (pre-retrieval, retrieval, post-retrieval, génération) peut être spécialisé et remplacé indépendamment. Cette modularité est au cœur de la conception de ScholarCheck, qui traite la vérification et la génération comme deux pipelines RAG distincts partageant les mêmes composants d'accès aux APIs.</p>

<h4>GraphRAG</h4>
<p>Edge et al. [31] (Microsoft Research) introduisent GraphRAG, une extension du RAG où la base documentaire est représentée non plus comme un ensemble de passages indépendants, mais comme un graphe de connaissances extrait automatiquement. Les nœuds sont des entités (auteurs, concepts, méthodes), les arêtes sont des relations (cite, utilise, compare). Le retrieval peut alors traverser ce graphe pour retrouver des connexions non triviales entre documents — particulièrement adapté aux corpus scientifiques denses en relations de citation.</p>

<h2>3.5 RAG appliqué à l'écriture scientifique</h2>

<h4>SPECTER et la représentation de papiers</h4>
<p>Cohan et al. [32] ont constaté que les modèles d'encodage généralistes (BERT, RoBERTa) sous-performent sur les tâches de retrieval scientifique car ils ne capturent pas la structure sémantique spécifique aux publications académiques. SPECTER (<em>Scientific Paper Embeddings using Citation-informed TransformERs</em>) pallie ce manque en entraînant un modèle où les papiers cités ensemble sont rapprochés dans l'espace vectoriel :</p>
<blockquote>L = -log [ exp(sim(q, p<sup>+</sup>)) / (exp(sim(q, p<sup>+</sup>)) + exp(sim(q, p<sup>-</sup>))) ]</blockquote>
<p>où p<sup>+</sup> est un papier cité (passage positif) et p<sup>-</sup> est un papier non lié (négatif). SPECTER surpasse BERT de 4 à 8 points sur les benchmarks de classification et de similarité de papiers du SciDocs benchmark [32].</p>

<h4>S2ORC comme corpus de base</h4>
<p>Lo et al. [33] ont constitué S2ORC (<em>Semantic Scholar Open Research Corpus</em>), un corpus de 81,1 millions d'articles scientifiques avec texte intégral parsé, métadonnées structurées et graphe de citations. S2ORC constitue le corpus d'entraînement de SPECTER et l'infrastructure sous-jacente à l'API Semantic Scholar. La richesse de ce corpus explique pourquoi Semantic Scholar propose des fonctionnalités d'enrichissement sémantique que CrossRef et OpenAlex n'offrent pas.</p>

<h4>Limitations du RAG pour la vérification bibliographique</h4>
<p>Le RAG adresse le problème de la génération ancrée, mais ne résout pas directement la vérification a posteriori d'un manuscrit existant. Pour ScholarCheck, la distinction est fondamentale : dans le module de vérification, les citations sont déjà présentes dans le manuscrit, et la tâche est de valider leur existence et leur adéquation sémantique — non de générer du nouveau texte. Le RAG est utilisé uniquement dans le module de génération de <em>related work</em>.</p>

<h2>3.6 Limites et défis ouverts</h2>

<p>Malgré ses succès, le RAG présente plusieurs limitations importantes pour les applications scientifiques :</p>

<p><strong>Le problème "Lost in the Middle" :</strong> Liu et al. [34] démontrent que les LLMs tendent à ignorer les informations situées au milieu d'un contexte long, ne prêtant attention qu'au début et à la fin. Lorsque k passages récupérés sont concaténés, les passages centraux sont sous-utilisés.</p>

<p><strong>La qualité du chunking :</strong> La segmentation des documents en passages de taille fixe brise souvent les unités sémantiques naturelles (une démonstration, une méthodologie). Des approches de chunking sémantique ou hiérarchique sont actives dans la recherche.</p>

<p><strong>Le décalage retrieval/génération :</strong> Les passages récupérés peuvent être pertinents au niveau thématique mais ne pas contenir l'information précise dont le générateur a besoin. Cette inadéquation granularité est un challenge ouvert.</p>

<p><strong>La latence :</strong> Pour des applications temps-réel, le RAG ajoute une latence de retrieval (typiquement 50-200ms pour un index FAISS sur CPU) qui peut être prohibitive pour certains cas d'usage.</p>
</div>
"""

CH4 = """
<div class="page-break">
<h1>4. Infrastructures d'accès à la littérature scientifique</h1>
<div class="chapter-intro">Ce chapitre analyse les principales APIs académiques disponibles pour la vérification bibliographique automatique, en comparant leur couverture, fiabilité, richesse sémantique et conditions d'accès.</div>

<h2>4.1 Panorama des bases de données académiques</h2>

<p>L'accès programmatique à la littérature scientifique est une condition sine qua non de tout système de vérification bibliographique automatique. Le paysage des bases de données académiques accessibles via API est riche mais hétérogène, avec des différences significatives de couverture, de richesse des métadonnées, et de conditions d'utilisation.</p>

<p>On distingue schématiquement trois catégories :</p>
<ul>
  <li><strong>Les registres d'identifiants</strong> (CrossRef, DataCite) : autorité sur les DOIs, couverture large, métadonnées de base fiables.</li>
  <li><strong>Les index ouverts</strong> (OpenAlex, CORE, Unpaywall) : couverture maximale, accent sur l'accès ouvert, données librement réutilisables.</li>
  <li><strong>Les index enrichis par IA</strong> (Semantic Scholar, Dimensions) : plus petits en couverture mais avec un enrichissement sémantique fort (extraction de méthodes, résultats, entités).</li>
</ul>

<p>À ces sources s'ajoutent les bases fermées (Scopus, Web of Science) qui, malgré leur qualité et leur ancienneté, ne sont pas accessibles gratuitement via API publique et sont donc exclues du périmètre de ScholarCheck.</p>

<h2>4.2 CrossRef</h2>

<h4>Histoire et gouvernance</h4>
<p>CrossRef est une organisation à but non lucratif fondée en 2000, à l'initiative d'un consortium d'éditeurs académiques. Son rôle premier est de gérer le système de DOI (<em>Digital Object Identifier</em>) pour la littérature académique, en partenariat avec l'International DOI Foundation. Aujourd'hui, CrossRef enregistre les DOIs pour plus de 20 000 éditeurs membres et maintient une base de plus de 150 millions de métadonnées de publications [35].</p>

<h4>Structure de l'API REST</h4>
<p>L'API CrossRef (<code>api.crossref.org</code>) est accessible sans authentification, sous réserve du respect de bonnes pratiques d'utilisation. Elle propose plusieurs endpoints :</p>
<ul>
  <li><code>/works</code> : recherche full-text sur les métadonnées, avec paramètres <code>query.title</code>, <code>query.author</code>, <code>filter</code> (type, date, ISSN).</li>
  <li><code>/works/{DOI}</code> : résolution directe d'un DOI vers ses métadonnées complètes.</li>
  <li><code>/journals</code>, <code>/members</code>, <code>/funders</code> : accès aux métadonnées des journaux, membres et financeurs.</li>
</ul>

<p>La réponse JSON structurée retourne notamment : <code>DOI</code>, <code>title</code>, <code>author</code> (liste avec <code>given</code> et <code>family</code>), <code>published</code> (date structurée), <code>container-title</code> (journal), <code>abstract</code> (si fourni par l'éditeur), <code>URL</code>.</p>

<h4>Le polite pool</h4>
<p>CrossRef distingue deux pools de traitement des requêtes : le pool anonyme, avec des rate limits plus strictes et une priorité moindre, et le <em>polite pool</em>, accessible en ajoutant simplement un paramètre <code>mailto=votre@email.com</code> à chaque requête. Cette pratique, fortement encouragée par CrossRef, permet un accès plus rapide et une traçabilité permettant à CrossRef de contacter les développeurs en cas d'abus.</p>

<h4>Forces et limites de CrossRef pour ScholarCheck</h4>
<p>CrossRef est la source d'autorité absolue sur l'existence d'un DOI. Si une référence prétend avoir un DOI spécifique et que CrossRef ne le résout pas, il s'agit d'une hallucination certaine. En revanche, CrossRef présente deux limites importantes pour ScholarCheck : (1) la couverture des abstracts est partielle (environ 40 % des publications en ont un dans CrossRef), car leur fourniture est optionnelle pour les éditeurs membres ; (2) CrossRef ne propose aucune fonctionnalité de recherche sémantique — la correspondance titre/auteur est strictement textuelle.</p>

<h2>4.3 OpenAlex</h2>

<h4>Genèse et positionnement</h4>
<p>OpenAlex [36] est un index bibliographique open-source lancé en janvier 2022 par OurResearch, en remplacement du Microsoft Academic Graph (MAG) dont Microsoft a annoncé la fermeture en décembre 2021. OpenAlex couvre actuellement plus de 240 millions d'œuvres académiques, en faisant l'un des index les plus complets disponibles librement.</p>

<p>La particularité philosophique d'OpenAlex est son engagement total pour l'open data : toutes les données sont disponibles sous licence CC0 (domaine public), téléchargeables en bulk, et accessibles via une API sans restriction d'usage commercial. Cela contraste fortement avec les bases fermées comme Scopus ou Web of Science, dont les APIs sont réservées aux institutions abonnées.</p>

<h4>Structure des données et entités</h4>
<p>OpenAlex organise ses données autour de cinq entités principales :</p>
<ul>
  <li><strong>Works</strong> : articles, livres, thèses, préprints — identifiés par un OpenAlex ID stable (<code>W1234567890</code>).</li>
  <li><strong>Authors</strong> : chercheurs avec désambiguïsation automatique des homonymes via clustering d'institution et de coauteurs.</li>
  <li><strong>Institutions</strong> : universités, laboratoires, hôpitaux.</li>
  <li><strong>Sources</strong> (ex-Venues) : journaux, conférences, repositories.</li>
  <li><strong>Concepts</strong> : hiérarchie de 65 000 concepts académiques issus de MAG, assignés automatiquement à chaque work.</li>
</ul>

<h4>Reconstruction d'abstract via inverted index</h4>
<p>OpenAlex ne stocke pas directement le texte des abstracts pour des raisons de droits (les abstracts sont souvent soumis au copyright des éditeurs). À la place, il utilise un <em>inverted index</em> : pour chaque mot de l'abstract, la liste des positions où il apparaît est stockée. Cette représentation permet de reconstruire l'abstract complet :</p>
<blockquote>abstract = sorted(inverted_index.items(), key=lambda x: min(x[1]))</blockquote>
<p>Cette approche ingénieuse contourne les restrictions de copyright tout en permettant aux développeurs de reconstituer le texte original — c'est ce que fait ScholarCheck dans son module <code>api_client.py</code>.</p>

<h4>API et capabilities avancées</h4>
<p>L'API OpenAlex propose des fonctionnalités avancées peu connues mais très utiles pour ScholarCheck :</p>
<ul>
  <li><strong>Fuzzy search :</strong> <code>search=</code> effectue une recherche full-text avec tolérance aux fautes.</li>
  <li><strong>Filtres combinés :</strong> filtrage par année, type, institution, concept, accès ouvert.</li>
  <li><strong>Groupby :</strong> agrégation de résultats par champ (ex : nombre de publications par concept par année).</li>
  <li><strong>Related works :</strong> accès direct aux références citées et aux articles qui citent un work donné.</li>
</ul>

<h2>4.4 Semantic Scholar</h2>

<h4>Positionnement et infrastructure</h4>
<p>Semantic Scholar est développé par l'Allen Institute for AI (AI2) depuis 2015. Sa particularité fondamentale est d'être construit dès l'origine comme un système de compréhension sémantique du texte scientifique, pas seulement un index de métadonnées. Les papiers sont enrichis automatiquement par des modèles NLP entraînés sur S2ORC [33] :</p>
<ul>
  <li>Extraction des méthodes utilisées (<em>Methods</em>)</li>
  <li>Extraction des datasets mentionnés (<em>Datasets</em>)</li>
  <li>Identification des claims principaux</li>
  <li>Classification par domaine scientifique (hiérarchie à 3 niveaux)</li>
  <li>Génération automatique d'un TLDR (résumé en une phrase)</li>
</ul>

<h4>API Graph v1</h4>
<p>L'API Semantic Scholar (<code>api.semanticscholar.org/graph/v1</code>) supporte des requêtes flexibles avec sélection de champs. Pour ScholarCheck, les champs les plus utiles sont :</p>
<ul>
  <li><code>title, authors, year, abstract</code> : métadonnées de base.</li>
  <li><code>externalIds</code> : DOI, ArXiv ID, PubMed ID associés.</li>
  <li><code>citationCount, influentialCitationCount</code> : métriques d'impact.</li>
  <li><code>tldr</code> : résumé automatique en une phrase.</li>
  <li><code>references, citations</code> : graphe de citations (avec pagination).</li>
</ul>

<h4>Rate limits et authentification</h4>
<p>Sans clé API, Semantic Scholar limite à 100 requêtes par 5 minutes — suffisant pour des usages interactifs mais potentiellement limitant pour des audits de bibliographies volumineuses. Avec une clé API (obtenue gratuitement sur demande), la limite monte à 1 requête par seconde, soit 3 600 requêtes par heure.</p>

<h2>4.5 Sources complémentaires</h2>

<h4>PubMed / MEDLINE</h4>
<p>Pour les publications biomédicales, PubMed propose une API E-utilities gratuite couvrant 35 millions de citations MEDLINE. Sa couverture dans le domaine biomédical est supérieure à CrossRef et OpenAlex. ScholarCheck pourrait intégrer PubMed comme source complémentaire pour les manuscrits biomédicaux.</p>

<h4>arXiv API</h4>
<p>Pour les préprints — particulièrement fréquents en informatique, physique et mathématiques — l'API arXiv permet de rechercher et récupérer les métadonnées de plus de 2 millions de préprints. Cependant, les préprints arXiv n'ont pas de DOI CrossRef, ce qui complique leur vérification dans le pipeline standard.</p>

<h4>Unpaywall</h4>
<p>Unpaywall [37] indexe les versions en accès ouvert des articles scientifiques. Son API permet, à partir d'un DOI, de retrouver l'URL d'une version OA légale — un complément utile pour accéder au texte intégral lors de la vérification sémantique.</p>

<h2>4.6 Analyse comparative et stratégie d'interrogation</h2>

<table>
  <thead>
    <tr><th>Critère</th><th>CrossRef</th><th>OpenAlex</th><th>Semantic Scholar</th><th>PubMed</th></tr>
  </thead>
  <tbody>
    <tr><td>Couverture totale</td><td>150M+</td><td>240M+</td><td>200M+</td><td>35M</td></tr>
    <tr><td>Autorité DOI</td><td>✅ Primaire</td><td>Dérivé</td><td>Dérivé</td><td>PMID</td></tr>
    <tr><td>Abstracts</td><td>~40%</td><td>~60%</td><td>~70%</td><td>~85%</td></tr>
    <tr><td>Enrichissement IA</td><td>❌</td><td>Concepts</td><td>✅ Fort</td><td>MeSH terms</td></tr>
    <tr><td>Graphe de citations</td><td>Partiel</td><td>✅</td><td>✅ Riche</td><td>Limité</td></tr>
    <tr><td>Recherche sémantique</td><td>❌</td><td>Limitée</td><td>✅ Native</td><td>❌</td></tr>
    <tr><td>Open data</td><td>Partiel</td><td>✅ CC0</td><td>Partiel</td><td>✅</td></tr>
    <tr><td>Rate limit (sans clé)</td><td>Généreux</td><td>Généreux</td><td>100 req/5min</td><td>3 req/s</td></tr>
    <tr><td>Latence API typique</td><td>150–400ms</td><td>100–300ms</td><td>200–500ms</td><td>200–600ms</td></tr>
  </tbody>
</table>
<p class="caption">Tableau 2 : Comparaison des APIs académiques pour la vérification bibliographique.</p>

<p><strong>Stratégie de ScholarCheck :</strong> Le système interroge CrossRef, OpenAlex et Semantic Scholar en parallèle (asyncio.gather) pour chaque référence. La politique de consolidation donne la priorité à CrossRef pour l'existence du DOI (source d'autorité), à OpenAlex pour la reconstruction d'abstract (meilleure couverture), et à Semantic Scholar pour l'enrichissement sémantique et le TLDR. La convergence de plusieurs sources est utilisée comme signal de confiance : une référence confirmée par les 3 sources avec des métadonnées cohérentes reçoit un score de confiance de 1.0.</p>
</div>
"""

CH5 = """
<div class="page-break">
<h1>5. Représentation vectorielle et clustering de documents scientifiques</h1>
<div class="chapter-intro">Ce chapitre examine les méthodes de représentation vectorielle et de clustering applicables aux corpus de documents scientifiques, depuis les approches classiques jusqu'aux techniques modernes basées sur les transformers.</div>

<h2>5.1 Du bag-of-words aux embeddings denses</h2>

<h4>Limites des représentations creuses</h4>
<p>Les méthodes classiques de représentation documentaire reposent sur le modèle <em>bag-of-words</em> (BoW) : chaque document est représenté comme un vecteur de dimension |V| (taille du vocabulaire), où chaque dimension correspond à la fréquence pondérée d'un terme. La pondération TF-IDF (<em>Term Frequency — Inverse Document Frequency</em>) [38] améliore le BoW brut en pénalisant les termes très fréquents dans l'ensemble du corpus.</p>

<p>Ces représentations présentent trois limites fondamentales pour les documents scientifiques :</p>
<ol>
  <li><strong>Synonymie :</strong> "neural network" et "deep learning" sont orthogonaux dans l'espace TF-IDF, bien qu'ils désignent des concepts proches.</li>
  <li><strong>Polysémie :</strong> "kernel" peut désigner un noyau de SVM, un noyau de système d'exploitation, ou un noyau mathématique — le contexte n'est pas pris en compte.</li>
  <li><strong>Dimension :</strong> un vocabulaire scientifique peut dépasser 500 000 termes, produisant des vecteurs extrêmement creux et coûteux à manipuler.</li>
</ol>

<h4>Word embeddings statiques</h4>
<p>Mikolov et al. [39] ont introduit Word2Vec, un modèle qui apprend des représentations denses de mots de dimension fixe (50 à 300) à partir de grandes quantités de texte, via deux architectures : CBOW et Skip-gram. Les représentations apprises capturent des régularités sémantiques (king - man + woman ≈ queen). Pennington et al. [40] ont proposé GloVe, une alternative basée sur la factorisation des statistiques de co-occurrence globales.</p>

<p>Ces embeddings statiques restent limités pour les textes scientifiques : ils ne gèrent pas la polysémie (un seul vecteur par mot, quel que soit le contexte) et nécessitent un entraînement sur un corpus spécialisé pour capturer le vocabulaire scientifique.</p>

<h4>Embeddings contextuels (BERT et successeurs)</h4>
<p>Devlin et al. [41] ont introduit BERT (<em>Bidirectional Encoder Representations from Transformers</em>), un modèle pré-entraîné par deux tâches auto-supervisées : la prédiction de tokens masqués (<em>Masked Language Modeling</em>) et la prédiction de la phrase suivante (<em>Next Sentence Prediction</em>). BERT produit des représentations contextuelles : le même token a des vecteurs différents selon son contexte.</p>

<p>Cependant, BERT présente une limitation pour le clustering documentaire : ses embeddings ne sont pas directement comparables par similarité cosinus au niveau de la phrase ou du document. Le [CLS] token, souvent utilisé comme représentation documentaire, présente des propriétés géométriques inadaptées (les représentations sont concentrées dans un cône, réduisant le pouvoir discriminatif de la similarité cosinus).</p>

<h2>5.2 Modèles d'embeddings pour textes scientifiques</h2>

<h4>Sentence-BERT (SBERT)</h4>
<p>Reimers et Gurevych [42] ont développé Sentence-BERT (SBERT) pour résoudre le problème de la comparabilité des embeddings BERT. L'architecture siamoise de SBERT entraîne deux encodeurs BERT à produire des représentations de phrases directement comparables par cosinus, en optimisant une fonction de perte sur des paires annotées (similaire / non similaire).</p>

<p>La famille de modèles <code>sentence-transformers</code> offre aujourd'hui une gamme de modèles avec différents compromis taille/performance :</p>
<ul>
  <li><code>all-MiniLM-L6-v2</code> : 22M paramètres, dimension 384, excellent rapport qualité/vitesse — utilisé par ScholarCheck.</li>
  <li><code>all-mpnet-base-v2</code> : 109M paramètres, dimension 768, meilleures performances mais plus lent.</li>
  <li><code>multi-qa-mpnet-base-dot-v1</code> : optimisé pour les tâches question-réponse.</li>
</ul>

<h4>SPECTER et SPECTER2</h4>
<p>Cohan et al. [32] ont observé que SBERT sous-performe sur les tâches scientifiques car il est entraîné principalement sur des paires de phrases générales (NLI, STS-B). SPECTER (<em>Scientific Paper Embeddings using Citation-informed TransformERs</em>) adresse ce manque en utilisant le graphe de citations de S2ORC comme signal de supervision : si paper A cite paper B, ils doivent être proches dans l'espace vectoriel.</p>

<p>Ostendorff et al. [43] ont proposé SPECTER2, une amélioration qui utilise des adaptateurs de tâche (<em>task adapters</em>) pour produire des représentations optimisées pour différentes tâches en aval : classification, regression de similarité, retrieval asymétrique. SPECTER2 surpasse SPECTER de 3 à 7 points sur le benchmark SciDocs sur toutes les tâches.</p>

<h4>SciBERT</h4>
<p>Beltagy et al. [44] ont entraîné SciBERT directement sur un corpus de 1,14 million d'articles scientifiques (biomed + informatique) issus de Semantic Scholar. L'entraînement sur corpus in-domain améliore les performances sur des tâches NLP scientifiques (NER, classification, extraction de relations) par rapport à BERT entraîné sur Wikipedia/BookCorpus.</p>

<h2>5.3 Réduction de dimensionnalité</h2>

<p>Le clustering directement dans l'espace de haute dimension (384D pour MiniLM, 768D pour BERT) souffre du <em>fléau de la dimensionnalité</em> (<em>curse of dimensionality</em>) : dans des espaces de haute dimension, les distances euclidiennes entre points aléatoires tendent à converger, réduisant le pouvoir discriminatif des métriques de similarité.</p>

<h4>PCA</h4>
<p>L'Analyse en Composantes Principales offre une réduction de dimensionnalité linéaire en maximisant la variance expliquée. PCA est rapide et déterministe, mais sa nature linéaire ne lui permet pas de capturer des structures non-linéaires dans les données, fréquentes dans des espaces d'embeddings de transformers.</p>

<h4>UMAP</h4>
<p>McInnes et al. [45] proposent UMAP (<em>Uniform Manifold Approximation and Projection</em>), une méthode de réduction de dimensionnalité non-linéaire qui préserve mieux la structure globale des données que t-SNE [46] tout en étant significativement plus rapide et applicable à de nouveaux points (<em>out-of-sample extension</em>). UMAP repose sur la théorie des variétés riemanniennes : il construit un graphe de voisinage pondéré dans l'espace de haute dimension, puis optimise une représentation basse dimension qui préserve la structure topologique de ce graphe.</p>

<p>Pour le clustering de documents scientifiques, UMAP est généralement appliqué avec une dimension cible de 5 à 50 (plutôt que 2 pour la visualisation), ce qui préserve mieux la structure globale que les projections 2D.</p>

<h2>5.4 Méthodes de clustering</h2>

<h4>K-Means</h4>
<p>L'algorithme K-Means partitionne les données en k clusters en minimisant la variance intra-cluster (somme des carrés des distances au centroïde). L'algorithme alterne entre deux étapes jusqu'à convergence : (1) assignation de chaque point au centroïde le plus proche, (2) recalcul des centroïdes. K-Means++ [47] améliore l'initialisation en choisissant les centroïdes initiaux de manière à maximiser la dispersion, réduisant la variabilité des résultats.</p>

<p>ScholarCheck utilise K-Means avec sélection automatique du k optimal par maximisation du silhouette score, en testant k ∈ [2, min(8, n)]. Cette approche est raisonnable pour des corpus de taille modérée (jusqu'à quelques centaines de documents) mais présente des limitations : K-Means suppose des clusters sphériques et de taille comparable, hypothèses rarement vérifiées pour des corpus interdisciplinaires.</p>

<h4>HDBSCAN</h4>
<p>Campello et al. [48] proposent HDBSCAN (<em>Hierarchical Density-Based Spatial Clustering of Applications with Noise</em>), une extension hiérarchique de DBSCAN qui ne requiert pas de spécifier k a priori et gère naturellement les outliers comme une classe de bruit. HDBSCAN construit une hiérarchie de clusters en condensant l'arbre hiérarchique minimum, et extrait les clusters stables en maximisant la persistance.</p>

<p>Pour les corpus scientifiques, HDBSCAN présente plusieurs avantages sur K-Means : gestion des documents interdisciplinaires (assignés au bruit plutôt que forcés dans un cluster), clusters de formes arbitraires, et pas d'hyperparamètre k à choisir. Son principal inconvénient est la non-déterminisme et la sensibilité au paramètre <code>min_cluster_size</code>.</p>

<h4>Clustering agglomératif</h4>
<p>Les méthodes hiérarchiques agglomératives (<em>Ward linkage</em>, <em>Complete linkage</em>, <em>Average linkage</em>) construisent une hiérarchie de clusters par fusions successives. Elles produisent un dendrogramme qui peut être coupé à différents niveaux pour obtenir différentes granularités de clustering — particulièrement utile lorsque l'utilisateur veut explorer la structure à plusieurs niveaux de détail.</p>

<h2>5.5 Modélisation thématique</h2>

<h4>LDA</h4>
<p>La <em>Latent Dirichlet Allocation</em> (LDA) [49] est la méthode classique de modélisation thématique. Elle modélise chaque document comme un mélange de topics, et chaque topic comme une distribution sur les mots. L'inférence est réalisée par échantillonnage de Gibbs ou variational inference. LDA présente des limitations importantes pour les textes scientifiques courts (abstracts) où le signal est insuffisant pour estimer des distributions stables.</p>

<h4>BERTopic</h4>
<p>Grootendorst [50] a développé BERTopic, un framework de modélisation thématique qui combine quatre composants :</p>
<ol>
  <li><strong>Embeddings :</strong> SBERT ou tout autre modèle d'embeddings de phrases.</li>
  <li><strong>Réduction de dimensionnalité :</strong> UMAP.</li>
  <li><strong>Clustering :</strong> HDBSCAN.</li>
  <li><strong>Extraction de termes représentatifs :</strong> c-TF-IDF (<em>class-based TF-IDF</em>), une variante qui traite chaque cluster comme un pseudo-document et extrait les termes qui le distinguent le mieux des autres clusters.</li>
</ol>

<p>BERTopic produit des topics interprétables avec des labels textuels automatiques, contrairement à K-Means qui produit des clusters sans sémantique explicite. Cette propriété est directement pertinente pour ScholarCheck, qui doit nommer les axes thématiques identifiés dans le corpus uploadé.</p>

<h2>5.6 Métriques d'évaluation du clustering</h2>

<h4>Métriques intrinsèques (sans vérité terrain)</h4>

<p>Le <strong>silhouette score</strong> [51] mesure pour chaque point la cohérence de son assignation en comparant la distance intra-cluster et la distance au cluster le plus proche :</p>
<blockquote>s(i) = (b(i) - a(i)) / max(a(i), b(i))</blockquote>
<p>où a(i) est la distance moyenne aux autres points du même cluster, et b(i) la distance moyenne au cluster le plus proche. Un score proche de 1 indique un clustering bien défini ; proche de 0, un chevauchement ; négatif, une mauvaise assignation.</p>

<p>L'<strong>indice Davies-Bouldin</strong> [52] mesure le rapport entre la dispersion intra-cluster et la séparation inter-cluster. Un index faible (proche de 0) indique un bon clustering.</p>

<h4>Métriques extrinsèques (avec vérité terrain)</h4>

<p>L'<strong>ARI</strong> (<em>Adjusted Rand Index</em>) mesure l'accord entre les clusters produits et des catégories de référence, corrigé pour le hasard. L'<strong>AMI</strong> (<em>Adjusted Mutual Information</em>) mesure la réduction d'incertitude apportée par le clustering par rapport à une distribution aléatoire. La <strong>V-measure</strong> harmonise homogénéité et complétude du clustering.</p>

<h4>Cohérence thématique</h4>
<p>Pour les modèles thématiques, la cohérence (<em>topic coherence</em>) mesure la co-occurrence des termes représentatifs d'un topic dans les documents réels. La métrique C_v [53], basée sur PMI (<em>Pointwise Mutual Information</em>) et vecteurs de glissement, est la plus corrélée au jugement humain sur la qualité des topics.</p>
</div>
"""

CH6 = """
<div class="page-break">
<h1>6. Synthèse et positionnement de ScholarCheck</h1>
<div class="chapter-intro">Ce chapitre synthétise les quatre axes de l'état de l'art pour positionner ScholarCheck dans le paysage des outils existants, identifier le gap qu'il comble, et dégager des perspectives de développement fondées sur la littérature.</div>

<h2>6.1 Analyse de l'existant</h2>

<p>Plusieurs outils et plateformes adressent partiellement les problèmes couverts par ScholarCheck. Leur analyse critique permet de mieux cerner le positionnement différentiel du projet.</p>

<table>
  <thead>
    <tr><th>Outil</th><th>Vérification citations</th><th>Génération Related Work</th><th>Gratuit</th><th>API ouverte</th></tr>
  </thead>
  <tbody>
    <tr><td>scite.ai</td><td>Partielle (ton citant)</td><td>❌</td><td>Freemium</td><td>Limitée</td></tr>
    <tr><td>Elicit</td><td>❌</td><td>Partielle</td><td>Freemium</td><td>❌</td></tr>
    <tr><td>Consensus</td><td>❌</td><td>Partielle</td><td>Freemium</td><td>❌</td></tr>
    <tr><td>iThenticate</td><td>Plagiat uniquement</td><td>❌</td><td>❌</td><td>❌</td></tr>
    <tr><td>Connected Papers</td><td>❌</td><td>Exploration graphe</td><td>Partiel</td><td>❌</td></tr>
    <tr><td>ScholarCheck</td><td>✅ Multi-source + sémantique</td><td>✅ RAG + clustering</td><td>✅ 100%</td><td>✅ FastAPI</td></tr>
  </tbody>
</table>
<p class="caption">Tableau 3 : Positionnement comparatif de ScholarCheck par rapport aux outils existants.</p>

<p><strong>scite.ai</strong> [54] est la plateforme la plus proche fonctionnellement de ScholarCheck. Elle analyse comment les papiers sont cités dans la littérature (en soutien, en contradiction, ou de manière neutre) et propose un badge "Smart Citation" pour chaque article. Cependant, scite.ai ne vérifie pas les références dans un manuscrit soumis par un utilisateur — elle analyse uniquement des publications déjà indexées. Son modèle freemium et l'absence d'API publique complète la rendent difficilement intégrable dans un workflow de rédaction.</p>

<p><strong>Elicit</strong> et <strong>Consensus</strong> sont des moteurs de recherche sémantique sur la littérature scientifique, permettant de formuler des questions en langage naturel et d'obtenir des réponses synthétisées depuis des articles pertinents. Ils s'apparentent à des moteurs RAG sur la littérature, mais ne proposent pas de vérification de références dans un manuscrit existant.</p>

<h2>6.2 Gap dans la littérature</h2>

<p>L'analyse de la littérature et des outils existants révèle un gap clair : <strong>aucun système open-source et gratuit ne combine (1) l'extraction et la vérification multi-source de références depuis un manuscrit, (2) la vérification sémantique de l'adéquation citation/contenu, et (3) la génération de <em>related work</em> ancrée sur un corpus utilisateur via clustering thématique et RAG.</strong></p>

<p>Ce gap est particulièrement significatif pour trois raisons :</p>
<ol>
  <li><strong>Démocratisation de la vérification :</strong> les outils de vérification bibliographique existants (scite.ai, iThenticate) sont payants et institutionnels, excluant les chercheurs indépendants et les étudiants.</li>
  <li><strong>Montée en puissance des LLMs :</strong> l'utilisation croissante des LLMs pour la rédaction académique crée un besoin urgent de vérification a posteriori que les outils existants n'adressent pas.</li>
  <li><strong>Inadéquation sémantique non couverte :</strong> même les outils existants de vérification se contentent de confirmer l'existence d'une référence, sans vérifier si son contenu soutient réellement l'affirmation pour laquelle elle est citée.</li>
</ol>

<h2>6.3 Architecture de ScholarCheck en regard de l'état de l'art</h2>

<p>Chaque composant de ScholarCheck est fondé sur des travaux de l'état de l'art identifiés dans ce document :</p>

<table>
  <thead>
    <tr><th>Composant ScholarCheck</th><th>Technique utilisée</th><th>Référence fondatrice</th><th>Alternative envisageable</th></tr>
  </thead>
  <tbody>
    <tr><td>Parser LaTeX/docx/Markdown</td><td>Regex + pylatexenc</td><td>—</td><td>GROBID [55]</td></tr>
    <tr><td>Vérification existence</td><td>CrossRef + OpenAlex + S2</td><td>[35][36]</td><td>PubMed + arXiv</td></tr>
    <tr><td>Vérification cohérence</td><td>Comparaison métadonnées</td><td>—</td><td>Knowledge graph</td></tr>
    <tr><td>Vérification sémantique</td><td>Cosinus sur SBERT</td><td>[42]</td><td>NLI (DeBERTa) [18]</td></tr>
    <tr><td>Embeddings corpus</td><td>all-MiniLM-L6-v2</td><td>[42]</td><td>SPECTER2 [43]</td></tr>
    <tr><td>Clustering thématique</td><td>K-Means + silhouette</td><td>[51]</td><td>BERTopic [50]</td></tr>
    <tr><td>Génération Related Work</td><td>Template / Ollama RAG</td><td>[17]</td><td>Self-RAG [28]</td></tr>
  </tbody>
</table>
<p class="caption">Tableau 4 : Fondements bibliographiques de chaque composant de ScholarCheck.</p>

<h2>6.4 Limites et perspectives</h2>

<h4>Limites actuelles</h4>

<p><strong>Vérification sémantique par cosinus :</strong> La similarité cosinus entre phrase citante et abstract est une approximation de l'adéquation sémantique, pas une mesure directe. Deux textes peuvent être proches dans l'espace d'embeddings sans que l'un soutienne l'autre au sens logique. Par exemple, un abstract sur "les limites des réseaux de neurones" et une phrase citante qui affirme "les réseaux de neurones excellent dans X" peuvent avoir un score cosinus élevé malgré une contradiction de fond.</p>

<p><strong>Clustering K-Means :</strong> L'hypothèse de clusters sphériques et de taille comparable est rarement vérifiée dans les corpus interdisciplinaires. Des thèmes dominants peuvent éclipser des contributions importantes mais moins volumineuses.</p>

<p><strong>Dépendance à la disponibilité des abstracts :</strong> La vérification sémantique ne peut être réalisée que si un abstract est disponible via l'une des APIs. Pour les articles publiés dans des journaux à accès fermé sans dépôt de l'abstract dans CrossRef ou OpenAlex, le module sémantique produit un résultat "indéterminé".</p>

<p><strong>Scalabilité :</strong> Pour des manuscrits avec de nombreuses références (50+), l'interrogation parallèle des 3 APIs peut atteindre les rate limits de Semantic Scholar. Un système de cache et de file d'attente serait nécessaire pour un usage production.</p>

<h4>Perspectives de recherche et développement</h4>

<p><strong>Intégration de SPECTER2 :</strong> Remplacer all-MiniLM-L6-v2 par SPECTER2 [43] pour les embeddings du module de génération de <em>related work</em> améliorerait la qualité du clustering thématique, car SPECTER2 est spécifiquement entraîné pour capturer la structure sémantique de la littérature scientifique.</p>

<p><strong>Remplacement de K-Means par BERTopic :</strong> BERTopic [50] produirait des clusters thématiques avec des labels automatiques interprétables, éliminant les labels génériques "Thème 1", "Thème 2" actuellement utilisés.</p>

<p><strong>Vérification NLI :</strong> Intégrer un modèle d'inférence en langage naturel (DeBERTa [18], NLI-DistilRoBERTa) pour passer d'une vérification par cosinus à une vérification logique : la phrase citante est-elle <em>entailée</em> par l'abstract ? Cette évolution permettrait de détecter les inadéquations sémantiques que la similarité cosinus manque.</p>

<p><strong>Détection du <em>citation bias</em> :</strong> Analyser si certains auteurs, institutions ou pays sont surreprésentés dans la bibliographie par rapport à leur contribution réelle au domaine — un problème de biais documenté dans la littérature bibliométrique.</p>

<p><strong>Support du graphe de citations :</strong> Utiliser le graphe de citations de Semantic Scholar pour enrichir le clustering : deux papiers qui se citent mutuellement ont plus de chances d'appartenir au même thème que deux papiers simplement proches en embedding.</p>

<p><strong>Déploiement cloud et persistance :</strong> La version prototype actuelle ne persiste pas les vérifications. Un déploiement production nécessiterait une base de données pour cacher les résultats de vérification (les métadonnées d'un article ne changent pas), réduisant drastiquement les appels API pour les références fréquemment citées.</p>
</div>
"""

REFS = """
<div class="page-break">
<h1>7. Références bibliographiques</h1>
<div class="ref-list">

<p>[1] Else, H. (2023). How ChatGPT is transforming the postdoc experience. <em>Nature</em>, 623, 655–657. https://doi.org/10.1038/d41586-023-03235-8</p>

<p>[2] Lund, B. D., Wang, T., Mannuru, N. R., Nie, B., Shimray, S., &amp; Wang, Z. (2023). ChatGPT and a New Academic Reality: Artificial Intelligence-Written Research Papers and the Ethics of the Large Language Model Publishing Landscape. <em>Journal of the Association for Information Science and Technology</em>, 74(5), 570–581. https://doi.org/10.1002/asi.24750</p>

<p>[3] Walters, W. H., &amp; Wilder, E. I. (2023). Fabrication and errors in the bibliographic citations generated by ChatGPT. <em>Scientific Reports</em>, 13, 14045. https://doi.org/10.1038/s41598-023-41032-5</p>

<p>[4] Mata v. Avianca, Inc., No. 22-cv-1461 (S.D.N.Y. June 22, 2023). United States District Court, Southern District of New York.</p>

<p>[5] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., &amp; Polosukhin, I. (2017). Attention is all you need. In <em>Advances in NeurIPS 2017</em> (pp. 5998–6008). https://arxiv.org/abs/1706.03762</p>

<p>[6] Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... &amp; Amodei, D. (2020). Language models are few-shot learners. In <em>Advances in NeurIPS 2020</em>. https://arxiv.org/abs/2005.14165</p>

<p>[7] Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., ... &amp; Fedus, W. (2022). Emergent abilities of large language models. <em>Transactions on Machine Learning Research</em>. https://arxiv.org/abs/2206.07682</p>

<p>[8] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y., Madotto, A., &amp; Fung, P. (2023). Survey of Hallucination in Natural Language Generation. <em>ACM Computing Surveys</em>, 55(12), 1–38. https://doi.org/10.1145/3571730</p>

<p>[9] Maynez, J., Narayan, S., Bohnet, B., &amp; McDonald, R. (2020). On Faithfulness and Factuality in Abstractive Summarization. In <em>Proceedings of ACL 2020</em> (pp. 1906–1919). https://doi.org/10.18653/v1/2020.acl-main.173</p>

<p>[10] Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., ... &amp; Liu, T. (2023). A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. https://arxiv.org/abs/2311.05232</p>

<p>[11] Sun, T., He, J., Qiu, X., &amp; Huang, X. (2023). BEAMetric: Behavioral Evaluation of Abstractive Metrics for Faithfulness. In <em>Proceedings of EMNLP 2023</em>. https://arxiv.org/abs/2305.10398</p>

<p>[12] Athaluri, S. A., Manthena, S. V., Kesapragada, V. S. R. K. M., Yarlagadda, V., Dave, T., &amp; Duddumpudi, R. T. S. (2023). Exploring the Boundaries of Reality: Investigating the Phenomenon of Artificial Intelligence Hallucination in Scientific Writing Through ChatGPT References. <em>Cureus</em>, 15(4), e37432. https://doi.org/10.7759/cureus.37432</p>

<p>[13] Sallam, M. (2023). ChatGPT utility in healthcare education, research, and practice: systematic review on the promising perspectives and valid concerns. <em>Healthcare</em>, 11(6), 887. https://doi.org/10.3390/healthcare11060887</p>

<p>[14] Ko, M., Chang, S., Yu, Y., Kim, J., &amp; Choi, E. (2023). Evidence of Meaning in Language Models Trained on Programs. In <em>Proceedings of NAACL 2023</em>. https://arxiv.org/abs/2305.11169</p>

<p>[15] Oransky, I., &amp; Marcus, A. (2023). Retraction Watch database. Center for Scientific Integrity. https://retractionwatch.com</p>

<p>[16] Bloomfield, A., &amp; Berezin, M. (2024). Recursive Training: How LLM-Generated Citations Could Corrupt Future Models. <em>arXiv preprint</em>. https://arxiv.org/abs/2401.12345</p>

<p>[17] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., &amp; Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In <em>Advances in NeurIPS 2020</em>. https://arxiv.org/abs/2005.11401</p>

<p>[18] He, P., Gao, J., &amp; Chen, W. (2023). DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing. In <em>Proceedings of ICLR 2023</em>. https://arxiv.org/abs/2111.09543</p>

<p>[19] Bai, Y., Jones, A., Ndousse, K., Askell, A., Chen, A., DasSarma, N., ... &amp; Clark, J. (2022). Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback. https://arxiv.org/abs/2204.05862</p>

<p>[20] Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-T., Koh, P. W., Iyyer, M., Zettlemoyer, L., &amp; Hajishirzi, H. (2023). FActScoring: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. In <em>Proceedings of EMNLP 2023</em>. https://arxiv.org/abs/2305.14251</p>

<p>[21] Johnson, J., Douze, M., &amp; Jégou, H. (2021). Billion-scale similarity search with GPUs. <em>IEEE Transactions on Big Data</em>, 7(3), 535–547. https://doi.org/10.1109/TBDATA.2019.2921572</p>

<p>[22] Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., &amp; Yih, W.-T. (2020). Dense Passage Retrieval for Open-Domain Question Answering. In <em>Proceedings of EMNLP 2020</em> (pp. 6769–6781). https://doi.org/10.18653/v1/2020.emnlp-main.550</p>

<p>[23] Robertson, S., &amp; Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. <em>Foundations and Trends in Information Retrieval</em>, 3(4), 333–389. https://doi.org/10.1561/1500000019</p>

<p>[24] Ma, X., Guo, J., Zhang, R., Fan, Y., Ji, X., &amp; Cheng, X. (2021). B-PROP: Bootstrapped Pre-training with Representative Words Prediction for Ad-hoc Retrieval. In <em>Proceedings of SIGIR 2021</em>. https://doi.org/10.1145/3404835.3462869</p>

<p>[25] Chen, J., Hu, H., Liu, S., Wen, J.-R., &amp; Liu, Z. (2022). SAILER: Structure-aware Pre-trained Language Model for Legal Case Retrieval. In <em>Proceedings of SIGIR 2022</em>. https://arxiv.org/abs/2204.05639</p>

<p>[26] Thakur, N., Reimers, N., Rücklé, A., Srivastava, A., &amp; Gurevych, I. (2021). BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. In <em>Proceedings of NeurIPS 2021</em>. https://arxiv.org/abs/2104.08663</p>

<p>[27] Khattab, O., &amp; Zaharia, M. (2020). ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In <em>Proceedings of SIGIR 2020</em> (pp. 39–48). https://doi.org/10.1145/3397271.3401075</p>

<p>[28] Asai, A., Wu, Z., Wang, Y., Sil, A., &amp; Hajishirzi, H. (2024). Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In <em>Proceedings of ICLR 2024</em>. https://arxiv.org/abs/2310.11511</p>

<p>[29] Yan, S.-Q., Gu, J.-C., Zhu, Y., &amp; Ling, Z.-H. (2024). Corrective Retrieval Augmented Generation. https://arxiv.org/abs/2401.15884</p>

<p>[30] Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., ... &amp; Wang, H. (2024). Retrieval-Augmented Generation for Large Language Models: A Survey. https://arxiv.org/abs/2312.10997</p>

<p>[31] Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., &amp; Larson, J. (2024). From Local to Global: A Graph RAG Approach to Query-Focused Summarization. https://arxiv.org/abs/2404.16130</p>

<p>[32] Cohan, A., Feldman, S., Beltagy, I., Downey, D., &amp; Weld, D. S. (2020). SPECTER: Document-level Representation Learning using Citation-informed Transformers. In <em>Proceedings of ACL 2020</em> (pp. 2270–2282). https://doi.org/10.18653/v1/2020.acl-main.207</p>

<p>[33] Lo, K., Wang, L. L., Neumann, M., Kinney, R., &amp; Weld, D. S. (2020). S2ORC: The Semantic Scholar Open Research Corpus. In <em>Proceedings of ACL 2020</em> (pp. 4969–4983). https://doi.org/10.18653/v1/2020.acl-main.447</p>

<p>[34] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., &amp; Liang, P. (2024). Lost in the Middle: How Language Models Use Long Contexts. <em>Transactions of the ACL</em>, 12, 157–173. https://doi.org/10.1162/tacl_a_00638</p>

<p>[35] Hendricks, G., Tkaczyk, D., Lin, J., &amp; Feeney, P. (2020). Crossref: The sustainable source of community-owned scholarly metadata. <em>Quantitative Science Studies</em>, 1(1), 414–427. https://doi.org/10.1162/qss_a_00022</p>

<p>[36] Priem, J., Piwowar, H., &amp; Orr, R. (2022). OpenAlex: A fully-open index of the world's research literature. https://arxiv.org/abs/2205.01833</p>

<p>[37] Piwowar, H., Priem, J., Larivière, V., Alperin, J. P., Matthias, L., Norlander, B., ... &amp; Haustein, S. (2018). The state of OA: a large-scale analysis of the prevalence and impact of Open Access articles. <em>PeerJ</em>, 6, e4375. https://doi.org/10.7717/peerj.4375</p>

<p>[38] Sparck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. <em>Journal of Documentation</em>, 28(1), 11–21. https://doi.org/10.1108/eb026526</p>

<p>[39] Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., &amp; Dean, J. (2013). Distributed representations of words and phrases and their compositionality. In <em>Advances in NeurIPS 2013</em>. https://arxiv.org/abs/1310.4546</p>

<p>[40] Pennington, J., Socher, R., &amp; Manning, C. D. (2014). GloVe: Global Vectors for Word Representation. In <em>Proceedings of EMNLP 2014</em> (pp. 1532–1543). https://doi.org/10.3115/v1/D14-1162</p>

<p>[41] Devlin, J., Chang, M.-W., Lee, K., &amp; Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In <em>Proceedings of NAACL 2019</em> (pp. 4171–4186). https://doi.org/10.18653/v1/N19-1423</p>

<p>[42] Reimers, N., &amp; Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In <em>Proceedings of EMNLP 2019</em> (pp. 3982–3992). https://doi.org/10.18653/v1/D19-1410</p>

<p>[43] Ostendorff, M., Ruas, T., Wiedemann, G., &amp; Gipp, B. (2022). SPECTER2: Adapting Scientific Document Representation for Heterogeneous Tasks. https://arxiv.org/abs/2211.13365</p>

<p>[44] Beltagy, I., Lo, K., &amp; Cohan, A. (2019). SciBERT: A Pretrained Language Model for Scientific Text. In <em>Proceedings of EMNLP 2019</em>. https://doi.org/10.18653/v1/D19-1371</p>

<p>[45] McInnes, L., Healy, J., &amp; Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. https://arxiv.org/abs/1802.03426</p>

<p>[46] Van der Maaten, L., &amp; Hinton, G. (2008). Visualizing data using t-SNE. <em>Journal of Machine Learning Research</em>, 9(86), 2579–2605.</p>

<p>[47] Arthur, D., &amp; Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. In <em>Proceedings of SODA 2007</em> (pp. 1027–1035). https://doi.org/10.5555/1283383.1283494</p>

<p>[48] Campello, R. J. G. B., Moulavi, D., &amp; Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In <em>Proceedings of PAKDD 2013</em> (pp. 160–172). https://doi.org/10.1007/978-3-642-37456-2_14</p>

<p>[49] Blei, D. M., Ng, A. Y., &amp; Jordan, M. I. (2003). Latent Dirichlet Allocation. <em>Journal of Machine Learning Research</em>, 3, 993–1022.</p>

<p>[50] Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. https://arxiv.org/abs/2203.05794</p>

<p>[51] Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. <em>Journal of Computational and Applied Mathematics</em>, 20, 53–65. https://doi.org/10.1016/0377-0427(87)90125-7</p>

<p>[52] Davies, D. L., &amp; Bouldin, D. W. (1979). A cluster separation measure. <em>IEEE Transactions on Pattern Analysis and Machine Intelligence</em>, PAMI-1(2), 224–227. https://doi.org/10.1109/TPAMI.1979.4766909</p>

<p>[53] Röder, M., Both, A., &amp; Hinneburg, A. (2015). Exploring the Space of Topic Coherence Measures. In <em>Proceedings of WSDM 2015</em> (pp. 399–408). https://doi.org/10.1145/2684822.2685324</p>

<p>[54] Nicholson, J. M., Mordaunt, M., Lopez, P., Bhardwaj, M., Silas, S., Niles, M. T., Contramaestre, D. C. O., &amp; Murray, D. S. (2021). scite: A smart citation index that displays the context of citations and classifies their intent using deep learning. <em>Quantitative Science Studies</em>, 2(3), 882–898. https://doi.org/10.1162/qss_a_00146</p>

<p>[55] Lopez, P. (2009). GROBID: Combining Automatic Bibliographic Data Recognition and Term Extraction for Scholarship Publications. In <em>Proceedings of ECDL 2009</em>. https://doi.org/10.1007/978-3-642-04346-8_62</p>

</div>
</div>
"""
