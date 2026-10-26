# Independent camera evaluation protocol

This is a collection and evaluation plan, not evidence that camera accuracy has been measured. Public-data results from this project remain development comparisons: comparison-model exposure to some public sources is known or unresolved. Do not promote a replacement from those scores alone.

Capture on the user's target **A20 Pro iPhone Duo**, using that user-specified hardware designation. Record the actual device model identifier, OS/build, app/build, camera/lens and capture settings locally. This protocol makes no claim about official chip specifications. Evaluate the actual shipped Core ML artifacts on that device after conversion and parity checks; desktop predictions are a separate diagnostic.

## 1. Freeze the plan before model selection

- [ ] Assign a protocol version, local owner, seed and collection date range. Freeze the species list, sample targets, taxonomy, rejection policy, metrics and promotion criteria in a read-only local plan; record its SHA-256.
- [ ] Keep three separate partitions: camera calibration/validation, frozen camera test, and public development data. Allocate source groups before selecting checkpoints, thresholds or architectures using camera results. Keep test files and labels inaccessible to the training/selection process until the candidate and thresholds are frozen.
- [ ] Use the current species contract: 151 Kanto National Dex IDs, in bundled label order. Shiny and named regional variants map to the same underlying species, matching `protocol.json`; make no form-identification claim. Annotate every form separately. Define any additional Mega/Gigantamax treatment in the frozen plan before including those images. Later-generation species with different National Dex IDs are unknown negatives, even if related to a known species.
- [ ] Select checkpoint species for coverage and practical availability before inspecting model predictions. Include varied colors/shapes, small and large subjects, evolution families, and confusable pairs. Do not select species because a candidate already performs well on them. Record unavailable species explicitly.

## 2. Define independence at the original source

A new filename, camera angle, resize or session does not make a new independent specimen. Give each physical object, original card artwork, illustration, printed source and digital source image a stable local ID. The same card artwork in two cards, prints or screenshots is one artwork group. Two copies of the same figurine/plush design should share a design group even if they are different physical objects. Keep specimen IDs as finer metadata.

Connect records that share any original artwork, card artwork, object/design, video/burst or source photograph into one source group. That group belongs wholly to calibration or wholly to test. Independently enforce a second constraint: a capture session must be partition-specific, so do not photograph calibration and test specimens in the same session. Record the larger session blocks separately from source groups; a shared session can correlate many otherwise distinct sources. Photographs of one specimen across sessions stay together. When a source is reused through a screen or print, its identity follows the original source, not the display device.

Create the group registry and split assignment before capture. Check it against public training/development sources using original asset IDs where available, exact/decoded hashes, perceptual hashes and manual near-neighbor review. Exclude or quarantine matching public artwork from a strict independent test. If exposure cannot be resolved, mark it **unknown exposure** and report it separately. A freshly photographed public illustration tests capture changes, but does not establish novel artwork recognition.

Check exact/pixel/perceptual duplicate components again after capture, before opening predictions. Merge related groups without reference to model correctness. If a cross-partition connection appears, quarantine the entire component and replace its quota from a new source group. Record exclusions and reasons; never remove an image just because a model fails on it.

## 3. Collection targets

Counts below are practical minimum targets, not statistical guarantees. Multiple photographs of one group improve condition coverage; they do not multiply independent sample size.

| Frozen test scope | Known-species positives | Natural unrelated negatives | Unfamiliar-species negatives |
|---|---|---|---|
| First useful checkpoint | 30 predetermined species × 3 independent original object/artwork groups × 3 sessions = **270 retained photographs**, 90 source groups. | **100 independent source/object groups**, at least one original photo each. | At least 10 later-generation species × 2 independent groups = **20 groups/photos**. |
| Full 151-species evidence target | All 151 species × at least 5 independent original object/artwork groups × 3 sessions = **at least 2,265 retained photographs**, 755 source groups. | **At least 600 independent natural-object/scene groups/photos**. | At least 30 later-generation species × 2 independent groups × 2 sessions = **at least 120 photos**, 60 source groups. |

The 30-species checkpoint certifies no unobserved species. If fewer than all 151 species meet the full source-group target, report the exact coverage and missing IDs; do not describe that result as full-151 camera evidence. A large photo count from repeated artworks does not fill the group quota.

Keep additional calibration groups separate from those table counts. For the first checkpoint, target at least one additional original group per selected known species, 100 additional natural-negative groups and 20 additional unknown-species groups. For full coverage, target at least two additional positive groups per species, 200 natural-negative groups and 30 unknown-species groups. Increase calibration diversity when needed; never borrow test specimens or sessions to tune a threshold.

Each split should include physical cards, figurines/plush and screens/printed images where available. Record missing media per species; five artworks do not establish toy recognition. Aim for at least two media domains per species in the full test, with different source identities. Reuse of the same illustration across media stays one group and does not satisfy diversity quotas.

## 4. Capture conditions and difficult cases

For each positive group, retain one planned image from each of three separately scheduled sessions. Use a fixed capture recipe, such as: (1) clear frontal view in even light; (2) changed room/background, oblique view and distance; (3) low light or glare, partial hand occlusion or clutter. Record which condition was attempted and achieved. Avoid making every hard condition occur in just one session or one species. More photos are permitted under a frozen sampling rule; keep the entire burst and select a predetermined frame index, not the best-looking prediction.

- Include familiar confusions as **correctly labeled positives**: Nidoran female/male; Nidorina/Nidorino; Pikachu/Raichu; Abra/Kadabra/Alakazam; Poliwag/Poliwhirl/Poliwrath; and similar-colored/evolution relatives available in the collection. Report these pairs/families separately, with original-group support.
- Include shiny and regional versions of known species as positive form slices under the species mapping. A slice with no examples is unmeasured. Do not silently mix form-specific errors into a claim about the base form.
- Include unknown species with familiar silhouettes or relationships, such as later evolutions/relatives of Kanto species, alongside visually different unknown species. Use different original designs/artwork across calibration and test. Report unknown-species false accepts separately from natural-object false accepts.
- Natural negatives should cover empty/cluttered desks, rooms, outdoor scenes, people/hands, animals, plants, food, everyday objects and non-Pokémon toys/cartoon characters. Include plausible lookalikes and textures as well as easy empty backgrounds. Inspect them for incidental Pokémon art; label ambiguous/mixed scenes separately rather than calling them clean negatives.
- Include small subjects, off-center framing, background clutter, mild motion blur, glare and partial occlusion. Record multiple-Pokémon or unidentifiable scenes as a separate ambiguity slice with a predefined expected behavior. Do not force a single-species label onto them.

Capture original camera stills and preserve orientation metadata. Run the same images through baseline and candidate with the app's real orientation, crop, resize and confidence/rejection path. Also collect a separately labeled live-scanner slice if assessing live scanning. Do not substitute camera-roll screenshots for original captures. Synthetic rotations/blur are supplemental stress tests and inherit their original group.

## 5. Local provenance, permissions and manifests

Use photos taken for this evaluation by the user or a consenting collector who permits this local use. Keep permission notes and source/rights evidence locally. Record owner-created artwork or permission-cleared sources where possible; photographing a copyrighted card does not establish permission to redistribute its artwork. No public upload or redistribution is required by this protocol.

**Do not send private photos to chat, hosted inference, public repositories, model hubs or cloud evaluation services.** Store originals and labels in a local access-controlled directory outside tracked source files, with cloud synchronization disabled for that directory. Keep recognition offline and app scan photos in memory. Share only aggregate results and nonidentifying hashes when needed; keep paths, permission notes, faces, home details and GPS metadata private. Use cropped/redacted derivatives for any expressly authorized sharing, and keep their relationship to the original locally. Disable network access during capture/inference where practical; record that condition.

Maintain a local CSV/JSONL row per original image with at least:

| Field | Required content |
|---|---|
| Identity | `image_id`, local relative path, original-byte SHA-256, decoded-pixel SHA-256, dimensions, format, orientation. |
| Label | `dex_id` or null, canonical species, `expected_kind` (`known`, `unknown_species`, `natural_negative`, `ambiguous`), form and domain. |
| Grouping | `specimen_id`, `design_id`, `artwork_id`, source identity, `session_id`, final connected source `group_id`, session/batch block ID, assigned split. |
| Capture | Local capture date/session code, device/app/OS identifiers, lens/settings, condition, distance/angle bucket, occlusion/glare notes. Avoid public personal identifiers. |
| Provenance | Collector pseudonym, local permission-record ID, original creator/source reference, rights status, public-overlap status and review reason. |
| Integrity | Inclusion/exclusion status and reason, transform-parent ID where applicable, protocol version and label-review status. |

Have a knowledgeable reviewer label without seeing predictions. Independently review all ambiguous labels, forms, unknown species and disputed cases; keep the adjudication trail. Quarantine uncertain identities before freezing rather than guessing. Hash the sorted manifest, split assignment and label mapping; save the hashes and group counts with the experiment. Keep raw and decoded hashes distinct so orientation/conversion changes remain traceable.

## 6. Evaluate once, with uncertainty

Freeze candidate weights, Core ML artifact hash, label mapping, preprocessing, temperature/thresholds and selection record before unlocking test inference. Run both models on identical images. Preserve per-image predictions locally so paired errors can be audited without recapturing or changing labels after seeing scores.

Report top-1/top-3/top-5, macro recall, per-species support/confusions, acceptance coverage, accuracy among accepted known inputs, known-input false rejection and false acceptance on each negative category. Show both forced-choice and abstaining results. Report domain, lighting, form and confusable-family slices with sample/group counts. Give the baseline's shipped policy as a reference and a separately labeled validation-calibrated comparison where used; never choose either policy on test results.

Use paired uncertainty estimates that resample original independent groups, not individual photos. Show group-weighted results as well as image-weighted results. Session effects can remain correlated even after source grouping; report per-session results and a session-block sensitivity analysis. Confidence intervals with few groups will be wide. Zero observed false accepts is not proof of a zero false-accept rate.

Predeclare a practical accuracy improvement and acceptable false-accept/coverage tradeoff on calibration data. A replacement needs meaningful paired improvement without an unacceptable negative-input or important-slice regression, plus completed Apple parity and physical-device performance gates. Record cold/warm latency, sustained behavior, memory and thermal observations separately under the device protocol; accuracy evidence alone does not establish deployment fitness.

If the first checkpoint influences any model, augmentation or threshold decision, it becomes development evidence. A later clean confirmation must use new original groups and sessions never inspected during selection. Do not quietly reuse that checkpoint as the untouched portion of a final full-151 test. Keep each test opening, decision and subsequent benchmark version in the experiment log.

## Completion checklist

- [ ] Frozen protocol, split and label hashes exist; test access stayed closed until candidate/policy freeze.
- [ ] Source/artwork/object/session registry and cross-source overlap review are complete; no specimen/design/session crosses calibration and test.
- [ ] Original-group quotas and domain/form coverage are reported, including every missing species or slice.
- [ ] Label uncertainty, permissions and exclusions have local evidence; private images remain local.
- [ ] Baseline and candidate use identical inputs through the intended app pipeline on the recorded target device.
- [ ] Paired metrics, grouped uncertainty, false accepts, coverage and per-slice regressions are reported.
- [ ] Any previously inspected benchmark is identified as development evidence; promotion uses fresh untouched confirmation and completed device gates.
