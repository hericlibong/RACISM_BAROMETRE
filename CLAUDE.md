<!-- across-agent:start -->
## Rapport automatique pour Codex

Avant chacune de tes rÃ©ponses finales, Ã©cris ou remplace `.ai/claude-report.md` avec le mÃªme rapport que celui prÃ©sentÃ© Ã  lâ€™utilisateur.

Le rapport doit rester proportionnÃ© Ã  la demande et indiquer clairement : ce qui a Ã©tÃ© demandÃ©, ce qui a Ã©tÃ© fait, les fichiers modifiÃ©s, les vÃ©rifications effectuÃ©es et les Ã©ventuels points ouverts. Sâ€™il nâ€™y a eu aucune modification, indique-le simplement.

Fais-le automatiquement, sans demander une instruction de passation. Ne modifie jamais `.ai/codex-review.md`.
<!-- across-agent:end -->

<!-- roadmap:start -->
## Maintenance de la roadmap

`docs/ROADMAP.md` est le suivi de référence du projet. Avant toute tâche de projet :

1. Lis `docs/ROADMAP.md`.
2. Identifie les entrées concernées **avant d'agir**.

Après réalisation :

3. Mets à jour les cases et le statut, **après réalisation et vérification** — jamais avant.
4. Ajoute les nouvelles tâches ou décisions apparues pendant le travail.
5. Ne coche jamais une tâche incomplète ou non vérifiée.
6. Signale dans ton rapport final les éléments de roadmap modifiés.

Une question future ne bloque pas le projet sauf si la roadmap la désigne explicitement comme nécessaire à l'étape suivante. Les faits découverts peuvent conduire à rouvrir une phase déjà cadrée.

Le projet doit rester léger : ne fige ni outil, ni schéma technique, ni taxonomie, ni workflow complexe avant qu'une expérience réelle en démontre le besoin.

La source de vérité documentaire est `docs/`. Le registre des arbitrages est `docs/DECISIONS.md`.
<!-- roadmap:end -->

## Garde-fous — simplicité du baromètre

- Le projet n'est ni un fact-checker ni une enquête exhaustive.
- Pour chaque candidat, rechercher uniquement ce qui est nécessaire à l'admission, au rattachement, à la classification et à une formulation sans surinterprétation.
- Arrêter la recherche dès que ces opérations sont possibles, puis passer au candidat suivant.
- Ne pas résoudre une incertitude sans effet direct sur la décision, le rattachement, la classification ou la formulation.
- Garder le traitement proportionnel au candidat ; ne pas imposer une fiche complète à tous les cas.
- Ne pas ajouter de contrôle, champ, document ou étape sans besoin concret démontré.
- Privilégier la solution la plus simple assurant une qualification correcte et une traçabilité suffisante.
- Toute proposition qui augmente la complexité doit le signaler explicitement et justifier pourquoi cette complexité est nécessaire au fonctionnement concret du baromètre.

Principe directeur : **qualifier suffisamment pour le baromètre, puis passer au suivant.**
