import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, resolve, relative, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { gunzipSync } from 'node:zlib';
import { sha256 } from './lib/rom.mjs';
import { verifyAuraV3 } from './lib/verify-aura-v3.mjs';
import { verifyAuraV4 } from './lib/verify-aura-v4.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
const shortVideo = await json('evidence/youtube-short/validation.json');
assert(shortVideo.passed && shortVideo.width === 1080 && shortVideo.height === 1920 && shortVideo.seconds < 30);
assert(!shortVideo.gameplayTimeScaling && shortVideo.fullGameImagePreserved && shortVideo.nativeAudio);
assert.equal(sha256(await readFile(resolve(root, shortVideo.video.path))), shortVideo.video.sha256);
const gohanHitsRelease = await json('patches/release-v1-0-build-20261106-124607/manifest.json');
const gohanHitsValidation = await json('evidence/release-v1-0-build-20261106-124607/validation.json');
assert.equal(gohanHitsValidation.romSha256, gohanHitsRelease.target.sha256);
assert(gohanHitsValidation.passed && gohanHitsValidation.gohanCases.length === 12 && gohanHitsValidation.piccoloRegression.length === 12);
assert.deepEqual(gohanHitsValidation.comparison.map(x => x.maxHits), [2, 5]);
assert(gohanHitsValidation.comparison.every(x => x.damage === 34));
assert(!gohanHitsValidation.damageChanged && !gohanHitsValidation.animationChanged && !gohanHitsValidation.controlsChanged);
assert.equal(sha256(await readFile(resolve(root, gohanHitsRelease.patch.path))), gohanHitsRelease.patch.sha256);
assert.equal(sha256(await readFile(resolve(root, gohanHitsValidation.video.path))), gohanHitsValidation.video.sha256);
const fullPresentation = await json('evidence/presentation-full/validation.json');
assert(fullPresentation.passed && fullPresentation.takes === 26 && fullPresentation.roster.length === 11 && fullPresentation.stages === 9);
assert(!fullPresentation.romChanged && !fullPresentation.gameplayTimeScaling && fullPresentation.nativeAudio && fullPresentation.nativeHitsHud);
assert(fullPresentation.comboTakes === 8 && fullPresentation.meteorAndFinisherTakes === 9);
for (const media of fullPresentation.media) assert.equal(sha256(await readFile(resolve(root, media.path))), media.sha256);
assert(fullPresentation.media[1].bytes < 20 * 1024 * 1024);
const piccoloHitsRelease = await json('patches/release-v1-0-build-20261106-105411/manifest.json');
const piccoloHitsValidation = await json('evidence/release-v1-0-build-20261106-105411/validation.json');
assert.equal(piccoloHitsRelease.version, '1.0');
assert.equal(fullPresentation.romSha256, piccoloHitsRelease.target.sha256);
assert.equal(piccoloHitsValidation.romSha256, piccoloHitsRelease.target.sha256);
assert(piccoloHitsValidation.passed && piccoloHitsValidation.piccoloCases.length === 12);
assert.deepEqual(piccoloHitsValidation.comparison.map(x => x.maxHits), [2, 9]);
assert(piccoloHitsValidation.comparison.every(x => x.damage === 43));
assert.deepEqual(piccoloHitsValidation.crossGaps, [15, 18]);
assert(!piccoloHitsValidation.romCrossAnimationChanged && !piccoloHitsValidation.gameplayTimeScaling);
assert(piccoloHitsValidation.kiStartupTablesUnchanged && piccoloHitsValidation.damageUnchanged);
assert.equal(sha256(await readFile(resolve(root, piccoloHitsRelease.patch.path))), piccoloHitsRelease.patch.sha256);
for (const media of piccoloHitsValidation.media) assert.equal(sha256(await readFile(resolve(root, media.path))), media.sha256);
const kiStartupRelease = await json('patches/release-v1-0-build-20261106-103002/manifest.json');
const kiStartupValidation = await json('evidence/release-v1-0-build-20261106-103002/validation.json');
assert.equal(kiStartupRelease.version, '1.0');
assert.equal(kiStartupRelease.buildId, '20261106-103002');
assert.equal(kiStartupValidation.romSha256, kiStartupRelease.target.sha256);
assert(kiStartupValidation.passed && kiStartupValidation.techniqueCases === 16 && kiStartupValidation.postthrowPassed === 30);
assert(kiStartupValidation.damageAndDebitPreserved && kiStartupValidation.releaseAnimationUnitPreserved && !kiStartupValidation.projectileSpeedDataChanged);
assert.deepEqual(kiStartupValidation.crossovers, [2, 1]);
assert.equal(kiStartupValidation.crossMeteorHits, 3);
assert.equal(sha256(await readFile(resolve(root, kiStartupRelease.patch.path))), kiStartupRelease.patch.sha256);
for (const media of kiStartupValidation.media) assert.equal(sha256(await readFile(resolve(root, media.path))), media.sha256);
const releaseV1 = await json('patches/release-v1-0/manifest.json');
const releaseV1Validation = await json('evidence/release-v1-0/validation.json');
const releaseV1Promo = await json('evidence/release-v1-0/promo.json');
assert.equal(releaseV1.version, '1.0');
assert.equal(releaseV1.buildId, '20261106-100534');
assert.equal(releaseV1Validation.romSha256, releaseV1.target.sha256);
assert(releaseV1Validation.passed && releaseV1Validation.postThrowKiPassed === 120);
assert(releaseV1Validation.scriptedFrames === 88200 && releaseV1Validation.singleFramePollTests === 8);
assert(!releaseV1Validation.nativeCollisionChanges && !releaseV1Validation.nativeDamageChanges && !releaseV1Validation.stunFormulaChanges);
assert.equal(sha256(await readFile(resolve(root, releaseV1.patch.path))), releaseV1.patch.sha256);
assert.equal(releaseV1Promo.romSha256, releaseV1.target.sha256);
assert(!releaseV1Promo.gameplayTimeScaling && releaseV1Promo.nativeAudio && releaseV1Promo.nativeHitsHud);
assert.equal(sha256(await readFile(resolve(root, releaseV1Promo.video.path))), releaseV1Promo.video.sha256);
assert.deepEqual([1, 2, 4, 9].map(i => releaseV1Validation.clips[i].maxHits), [6, 3, 8, 13]);
const responsiveV2 = await json('patches/responsive-v2/manifest.json');
const responsiveV2Validation = await json('evidence/responsive-v2/validation.json');
assert(responsiveV2Validation.passed && responsiveV2Validation.inputPassed === 200);
assert(responsiveV2Validation.scriptedFrames === 88200 && responsiveV2Validation.stateRelocations === 168);
assert(responsiveV2Validation.romSha256 === responsiveV2.target.sha256);
assert(!responsiveV2Validation.counterRuleChanges && !responsiveV2Validation.nativeCollisionChanges);
assert(sha256(await readFile(resolve(root, responsiveV2.patch.path))) === responsiveV2.patch.sha256);
const responsiveManifest = await json('patches/responsive-v1/manifest.json');
const responsiveValidation = await json('evidence/responsive-v1/validation.json');
assert(responsiveValidation.passed && responsiveValidation.characters.length === 11);
assert(responsiveValidation.romSha256 === responsiveManifest.target.sha256);
assert(sha256(await readFile(resolve(root, responsiveManifest.patch.path))) === responsiveManifest.patch.sha256);
const responsiveBuild = await json('evidence/responsive-v1/build.json');
assert(Object.values(responsiveBuild.preserved).every(Boolean));
assert(Buffer.from((await readFile(resolve(root, 'src/gameplay/responsive-v1/responsive.hex'), 'utf8')).trim(), 'hex').length === responsiveBuild.codeBytes);
const comboSideTests = await json('evidence/combo-side-tests-v1/validation.json');
assert(comboSideTests.passed && !comboSideTests.romChanged && comboSideTests.videoTakes === 10 && comboSideTests.probeCases === 52);
assert(comboSideTests.allControlReturned && comboSideTests.allRequestedFinishersStarted && !comboSideTests.gameplayTimeScaling && !comboSideTests.hitsHudAdded);
assert.equal(comboSideTests.counterP2.player1Damage, 35);
assert.equal(comboSideTests.gokuGuardedMeteor.damage, 3);
assert.equal(sha256(await readFile(resolve(root, comboSideTests.video.path))), comboSideTests.video.sha256);
for (let i = 0; i < 10; i++) {
  const clip = await json(`evidence/combo-side-tests-v1/clip-${String(i).padStart(2, '0')}.json`);
  assert.equal(clip.romSha256, comboSideTests.romSha256);
  assert(clip.controlReturned && clip.expectedFinisherStarted !== false);
  assert.equal(sha256(await readFile(resolve(root, clip.trace.path))), clip.trace.sha256);
}
const hitsV3Manifest = await json('patches/hud-hits-v3/manifest.json');
assert.equal(sha256(await readFile(resolve(root, hitsV3Manifest.patch.path))), hitsV3Manifest.patch.sha256);
const hitsV3 = await json('evidence/hud-hits-v3/validation.json');
assert(hitsV3.passed && hitsV3.nativeHud && !hitsV3.postproductionCounter && !hitsV3.gameplayTimeScaling);
assert.equal(hitsV3.romSha256, hitsV3Manifest.target.sha256);
assert.equal(hitsV3.linkEligibleUpdates, 30);
assert.equal(hitsV3.displayEligibleUpdates, 90);
assert.deepEqual(hitsV3.isolatedPunchHitCounts, [1, 1, 1, 1, 1, 1]);
assert(hitsV3.expiredLinkWhileResultVisible && hitsV3.quickComboCrossMeteor === 6 && hitsV3.gokuMeteor === 3);
for (const record of hitsV3.records) {
  const bytes = await readFile(resolve(root, record.path));
  assert.equal(sha256(bytes), record.sha256);
  const report = JSON.parse(gunzipSync(bytes).toString('utf8'));
  assert(report.passed);
  assert.equal(report.romSha256, hitsV3Manifest.target.sha256);
}
for (const item of hitsV3.media) assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256);
for (let i = 0; i < 5; i++) {
  const clip = await json(`evidence/hud-hits-v3/clip-${String(i).padStart(2, '0')}.json`);
  assert(clip.controlReturned);
  assert.equal(clip.romSha256, hitsV3Manifest.target.sha256);
  const bytes = await readFile(resolve(root, clip.trace.path));
  assert.equal(sha256(bytes), clip.trace.sha256);
  assert.equal(JSON.parse(gunzipSync(bytes).toString('utf8')).length, clip.frames);
}
const hitsV3Static = await json('evidence/hud-hits-v3/static-validation.json');
assert.equal(hitsV3Static.outsideAllowedChangedBytes, 0);
assert(Object.values(hitsV3Static.preserved).every(Boolean));
assert.equal(hitsV3Static.targetSha256, hitsV3Manifest.target.sha256);
assert.equal(sha256(Buffer.from((await readFile(resolve(root, 'src/hud/hits-v3/hud.hex'), 'utf8')).trim(), 'hex')), hitsV3Static.codeSha256);
const shakePreview = await json('evidence/guard-shake-preview/manifest.json');
assert(!shakePreview.romModifiedForShake && shakePreview.postproductionShake && shakePreview.hudKeptSteady);
assert.equal(shakePreview.guardEvents.length, 3);
assert.equal(sha256(await readFile(resolve(root, shakePreview.video.path))), shakePreview.video.sha256);
const hitsV2Manifest = await json('patches/hud-hits-v2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, hitsV2Manifest.patch.path))), hitsV2Manifest.patch.sha256);
const hitsV2 = await json('evidence/hud-hits-v2/validation.json');
assert(hitsV2.passed && hitsV2.nativeHud && !hitsV2.postproductionCounter && !hitsV2.gameplayTimeScaling);
assert.equal(hitsV2.romSha256, hitsV2Manifest.target.sha256);
assert.equal(hitsV2.minimumVisibleHits, 2);
assert.equal(hitsV2.windowEligibleUpdates, 90);
assert(hitsV2.freezeDuringAttackAndDizzy && !hitsV2.crossAddsHits);
assert.equal(hitsV2.gokuMeteorContacts, 3);
assert.deepEqual(hitsV2.examples.map(e => e.activeMaximum), [3, 6, 10, 16, 3, 0, 3]);
for (const record of hitsV2.records) {
  const compressed = await readFile(resolve(root, record.path));
  assert.equal(sha256(compressed), record.sha256);
  const report = JSON.parse(gunzipSync(compressed).toString('utf8'));
  assert(report.passed);
  assert.equal(report.romSha256, hitsV2Manifest.target.sha256);
}
for (const item of hitsV2.media) assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256);
for (let i = 0; i < 7; i++) {
  const clip = await json(`evidence/hud-hits-v2/clip-${String(i).padStart(2, '0')}.json`);
  assert.equal(clip.romSha256, hitsV2Manifest.target.sha256);
  assert(clip.controlReturned);
  const bytes = await readFile(resolve(root, clip.trace.path));
  assert.equal(sha256(bytes), clip.trace.sha256);
  assert.equal(JSON.parse(gunzipSync(bytes).toString('utf8')).length, clip.frames);
}
const hitsV2Static = await json('evidence/hud-hits-v2/static-validation.json');
assert.equal(hitsV2Static.targetSha256, hitsV2Manifest.target.sha256);
assert.equal(hitsV2Static.outsideAllowedChangedBytes, 0);
assert(Object.values(hitsV2Static.preserved).every(Boolean));
assert.equal(sha256(Buffer.from((await readFile(resolve(root, 'src/hud/hits-v2/hud.hex'), 'utf8')).trim(), 'hex')), hitsV2Static.codeSha256);
const hitsV2Dizzy = await json('evidence/hud-hits-v2/dizzy-exit-validation.json');
assert(hitsV2Dizzy.passed && hitsV2Dizzy.reports.every(r => r.passed));
assert.equal(hitsV2Dizzy.romSha256, hitsV2Manifest.target.sha256);
const hitsManifest = await json('patches/hud-hits-v1/manifest.json');
assert.equal(sha256(await readFile(resolve(root, hitsManifest.patch.path))), hitsManifest.patch.sha256);
const hitsValidation = await json('evidence/hud-hits-v1/validation.json');
assert(hitsValidation.passed && hitsValidation.nativeHud && !hitsValidation.postproductionCounter && !hitsValidation.gameplayTimeScaling);
assert.equal(hitsValidation.romSha256, hitsManifest.target.sha256);
assert.equal(hitsValidation.minimumVisibleHits, 2);
assert(hitsValidation.singleHitsInternalOnly && hitsValidation.rosterRuntimeCases === 88 && hitsValidation.sideRegressionCases === 374);
assert.deepEqual(hitsValidation.examples, {gokuFlurry: 3, cellNeedleRush: 13, p2Meteor: 2, blockedMeteor: 0});
assert(hitsValidation.stunAccumulationFix.preservedThroughCellCrossAndSpecial && hitsValidation.stunAccumulationFix.normalInactivityResetValidated);
for (const record of hitsValidation.records) {
  const compressed = await readFile(resolve(root, record.path));
  assert.equal(sha256(compressed), record.sha256);
  const report = JSON.parse(gunzipSync(compressed).toString('utf8'));
  assert(report.passed);
  assert.equal(report.romSha256, hitsManifest.target.sha256);
}
for (const item of hitsValidation.media) assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256);
const hitsStatic = await json('evidence/hud-hits-v1/static-validation.json');
assert.equal(hitsStatic.targetSha256, hitsManifest.target.sha256);
assert.equal(hitsStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(hitsStatic.preserved).every(Boolean));
assert.equal(hitsStatic.minimumVisibleHits, 2);
for (const [file, expected] of [['hud.hex', hitsStatic.codeSha256], ['font.hex', hitsStatic.fontSha256]]) {
  assert.equal(sha256(Buffer.from((await readFile(resolve(root, 'src/hud/hits-v1', file), 'utf8')).trim(), 'hex')), expected);
}
const hitsDizzy = await json('evidence/hud-hits-v1/dizzy-exit-validation.json');
assert(hitsDizzy.passed && hitsDizzy.reports.every(r => r.passed));
assert.equal(hitsDizzy.romSha256, hitsManifest.target.sha256);
const sideAdvantage = await json('patches/side-advantage-v1/manifest.json');
assert.equal(sha256(await readFile(resolve(root, sideAdvantage.patch.path))), sideAdvantage.patch.sha256);
const advantageRuntime = await json('evidence/side-advantage-v1/runtime-validation.json');
assert(advantageRuntime.passed && advantageRuntime.jobs === 22 && advantageRuntime.inputTrials === 132 && advantageRuntime.liveCounterWindows > 0);
assert.equal(advantageRuntime.romSha256, sideAdvantage.target.sha256);
assert(advantageRuntime.reports.every(r => r.passed && r.results.every(t => t.passed)));
const advantageRegression = await json('evidence/side-advantage-v1/side-regression.json');
assert(advantageRegression.passed && advantageRegression.cases === 374);
assert.equal(advantageRegression.romSha256, sideAdvantage.target.sha256);
const advantageStatic = await json('evidence/side-advantage-v1/static-validation.json');
assert.equal(advantageStatic.targetSha256, sideAdvantage.target.sha256);
assert.equal(advantageStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(advantageStatic.preserved).every(Boolean));
assert.equal(sha256(Buffer.from((await readFile(resolve(root, 'src/gameplay/side-advantage-v1/side.hex'), 'utf8')).trim(), 'hex')), advantageStatic.codeSha256);
const advantageVideo = await json('evidence/side-advantage-v1/video-validation.json');
assert(advantageVideo.passed && advantageVideo.extraWindowActuallyEnabled && advantageVideo.liveCounterCrosses > 0 && !advantageVideo.gameplayTimeScaling);
assert.equal(advantageVideo.romSha256, sideAdvantage.target.sha256);
assert.equal(sha256(await readFile(resolve(root, advantageVideo.video.path))), advantageVideo.video.sha256);
const stunBreak = await json('patches/stun-break-v2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, stunBreak.patch.path))), stunBreak.patch.sha256);
const breakRuntime = await json('evidence/stun-break-v2/runtime-validation.json');
assert(breakRuntime.passed && breakRuntime.cases === 110 && breakRuntime.victimCharacters === 11);
assert.equal(breakRuntime.romSha256, stunBreak.target.sha256);
assert(breakRuntime.reports.every(r => r.passed && r.results.every(t => t.passed)));
const breakStatic = await json('evidence/stun-break-v2/static-validation.json');
assert.equal(breakStatic.targetSha256, stunBreak.target.sha256);
assert.equal(breakStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(breakStatic.preserved).every(Boolean));
assert.equal(sha256(Buffer.from((await readFile(resolve(root, 'src/gameplay/stun-break-v2/on-hit.hex'), 'utf8')).trim(), 'hex')), breakStatic.codeSha256);
const breakProjectile = await json('evidence/stun-break-v2/projectile-validation.json');
assert(breakProjectile.passed && breakProjectile.results.find(r => r.label === 'energy-blast').firstHit.timer === 0);
const breakMedia = await json('evidence/stun-break-v2/media.json');
assert.equal(breakMedia.romSha256, stunBreak.target.sha256);
for (const item of breakMedia.files) assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256);
const teleportExchange = await json('evidence/teleport-exchange-v1/validation.json');
assert(teleportExchange.passed && teleportExchange.successfulCrosses === 20 && teleportExchange.allCrossesZeroDamage);
assert(!teleportExchange.romModified && !teleportExchange.additionalReactionAdvantageImplemented && !teleportExchange.speedScaling);
assert.equal(sha256(await readFile(resolve(root, teleportExchange.video.path))), teleportExchange.video.sha256);
assert.equal(teleportExchange.romSha256, stunBreak.target.sha256);
const namekV2 = await json('research/palettes/namek-anime-v2.json');
assert(namekV2.onlyStage6ColorsAndChecksumChanged && namekV2.stage === 6);
assert.equal(namekV2.capture.romSha256, namekV2.targetSha256);
assert.equal(sha256(await readFile(resolve(root, 'assets/media/namek-anime-v2', namekV2.capture.file))), namekV2.capture.captureSha256);
const namekProposal = await json('evidence/stun-break-v2/namek-proposal-validation.json');
assert(namekProposal.passed && namekProposal.pendingUserSelection && namekProposal.onlyRecordedPaletteColorsAndChecksumChanged);
for (const capture of namekProposal.captures) assert.equal(sha256(await readFile(resolve(root, 'assets/media/namek-anime-v1', capture.file))), capture.captureSha256);
const stunHud = await json('patches/hud-stun-v1/manifest.json');
assert.equal(sha256(await readFile(resolve(root, stunHud.patch.path))), stunHud.patch.sha256);
for (const name of ['runtime-validation', 'side-regression']) {
  const report = await json(`evidence/hud-stun-v1/${name}.json`);
  assert(report.passed);
  assert.equal(report.romSha256, stunHud.target.sha256);
}
const stunHudTiming = await json('evidence/hud-stun-v1/timing-validation.json');
assert(stunHudTiming.passed && stunHudTiming.cases.length === 22);
assert.equal(stunHudTiming.targetSha256, stunHud.target.sha256);
const stunHudGraphics = await json('evidence/hud-stun-v1/graphics-validation.json');
assert(stunHudGraphics.passed && stunHudGraphics.fixedNativeHudIdenticalFrames === stunHudGraphics.frames);
assert.equal(stunHudGraphics.targetSha256, stunHud.target.sha256);
const visibleStunHud = await json('evidence/hud-stun-v1/visible-bars-validation.json');
assert(visibleStunHud.passed && visibleStunHud.samples.length === 16);
assert.equal(visibleStunHud.romSha256, stunHud.target.sha256);
const stunHudStatic = await json('evidence/hud-stun-v1/static-validation.json');
assert.equal(stunHudStatic.targetSha256, stunHud.target.sha256);
assert.equal(stunHudStatic.outsideAllowedChangedBytes, 0);
assert(!stunHudStatic.labels && stunHudStatic.newSprites === 2 && stunHudStatic.newRamAllocationBytes === 0);
assert(Object.values(stunHudStatic.preserved).every(Boolean));
const stunHudCode = Buffer.from((await readFile(resolve(root, 'src/hud/stun-v1/bars.hex'), 'utf8')).trim(), 'hex');
const stunHudResources = Buffer.from((await readFile(resolve(root, 'src/hud/stun-v1/resources.hex'), 'utf8')).trim(), 'hex');
assert.equal(sha256(stunHudCode), stunHudStatic.codeSha256);
assert.equal(sha256(stunHudResources), stunHudStatic.resourcesSha256);
const stunHudMedia = await json('evidence/hud-stun-v1/media-validation.json');
assert.equal(stunHudMedia.romSha256, stunHud.target.sha256);
assert(stunHudMedia.nativeHudIntegrated && !stunHudMedia.postproductionHud && !stunHudMedia.labels);
for (const item of stunHudMedia.files) assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256);
const nativeStunCombo = await json('patches/combos-v5-native-stun/manifest.json');
assert.equal(sha256(await readFile(resolve(root, nativeStunCombo.patch.path))), nativeStunCombo.patch.sha256);
for (const name of ['matrix', 'side-regression']) {
  const report = await json(`evidence/combos-v5-native-stun/${name}.json`);
  assert(report.passed);
  assert.equal(report.romSha256, nativeStunCombo.target.sha256);
}
const nativeStunTiming = await json('evidence/combos-v5-native-stun/timing-validation.json');
assert(nativeStunTiming.passed && nativeStunTiming.cases.length === 22);
assert.equal(nativeStunTiming.targetSha256, nativeStunCombo.target.sha256);
const nativeStunStatic = await json('evidence/combos-v5-native-stun/static.json');
assert.equal(nativeStunStatic.targetSha256, nativeStunCombo.target.sha256);
assert.equal(nativeStunStatic.outsideAllowedChangedBytes, 0);
assert(nativeStunStatic.noVictimCursorReset && nativeStunStatic.noReactionDurationHook);
assert(Object.values(nativeStunStatic.preserved).every(Boolean));
const nativeStunCode = Buffer.from((await readFile(resolve(root, 'src/gameplay/combos-v5-native-stun/combos.hex'), 'utf8')).trim(), 'hex');
assert.equal(sha256(nativeStunCode), nativeStunStatic.codeSha256);
assert.equal(nativeStunCode.length, nativeStunStatic.decodedBytes);
const naturalCombo = await json('patches/combos-v4-natural/manifest.json');
assert.equal(sha256(await readFile(resolve(root, naturalCombo.patch.path))), naturalCombo.patch.sha256);
for (const name of ['matrix', 'side-regression', 'finisher-validation']) {
  const report = await json(`evidence/combos-v4-natural/${name}.json`);
  assert(report.passed);
  assert.equal(report.romSha256, naturalCombo.target.sha256);
}
const naturalTiming = await json('evidence/combos-v4-natural/timing-validation.json');
assert(naturalTiming.passed && naturalTiming.cases.length === 22);
assert.equal(naturalTiming.targetSha256, naturalCombo.target.sha256);
const naturalStatic = await json('evidence/combos-v4-natural/static.json');
assert.equal(naturalStatic.targetSha256, naturalCombo.target.sha256);
assert.equal(naturalStatic.outsideAllowedChangedBytes, 0);
assert(naturalStatic.queueDoesNotResetOwnProgramActionCursor && naturalStatic.noInstantFollowupStep);
assert(Object.values(naturalStatic.preserved).every(Boolean));
const naturalCode = Buffer.from((await readFile(resolve(root, 'src/gameplay/combos-v4-natural/combos.hex'), 'utf8')).trim(), 'hex');
assert.equal(sha256(naturalCode), naturalStatic.codeSha256);
assert.equal(naturalCode.length, naturalStatic.decodedBytes);
const naturalVideo = await json('evidence/combos-v4-natural/video-validation.json');
assert.equal(naturalVideo.romSha256, naturalCombo.target.sha256);
assert(naturalVideo.nativeAudio && naturalVideo.durationSeconds >= 180 && naturalVideo.durationSeconds <= 300);
assert.equal(sha256(await readFile(resolve(root, naturalVideo.videoPath))), naturalVideo.sha256);
const genericCombo = await json('patches/combos-v3/manifest.json');
assert.equal(sha256(await readFile(resolve(root, genericCombo.patch.path))), genericCombo.patch.sha256);
for (const name of ['matrix', 'side-regression', 'repeat-validation']) {
  const report = await json(`evidence/combos-v3/${name}.json`);
  assert(report.passed);
  assert.equal(report.romSha256, genericCombo.target.sha256);
}
const genericStatic = await json('evidence/combos-v3/static.json');
assert.equal(genericStatic.targetSha256, genericCombo.target.sha256);
assert.equal(genericStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(genericStatic.preserved).every(Boolean));
const genericCode = Buffer.from((await readFile(resolve(root, 'src/gameplay/combos-v3/combos.hex'), 'utf8')).trim(), 'hex');
assert.equal(sha256(genericCode), genericStatic.codeSha256);
assert.equal(genericCode.length, genericStatic.decodedBytes);
const genericNative = await json('evidence/combos-v3/native-regression.json');
assert(genericNative.passed);
assert.equal(genericNative.targetSha256, genericCombo.target.sha256);
const genericFinishers = await json('evidence/combos-v3/finisher-validation.json');
assert.equal(genericFinishers.romSha256, genericCombo.target.sha256);
assert(genericFinishers.allElevenDownBConnectAfterABA);
const genericVideo = await json('evidence/combos-v3/video-validation.json');
assert.equal(genericVideo.romSha256, genericCombo.target.sha256);
assert(!genericVideo.counterInRom && !genericVideo.counterOverlay);
assert.equal(genericVideo.cases.length, 13);
assert(genericVideo.cases.every(item => item.matchesTraceHP && item.bothIdleAtEnd && item.romSha256 === genericCombo.target.sha256));
for (const item of genericVideo.files) assert.equal(sha256(await readFile(resolve(root, 'assets/media/combos-v3', item.filename))), item.sha256);
const kicks = await json('patches/combos-v2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, kicks.patch.path))), kicks.patch.sha256);
const kickMatrix = await json('evidence/combos-v2/matrix.json');
const kickSide = await json('evidence/combos-v2/side-regression.json');
const kickNative = await json('evidence/combos-v2/native-regression.json');
const kickStatic = await json('evidence/combos-v2/static.json');
assert(kickMatrix.passed && kickSide.passed && kickNative.passed);
assert.equal(kickMatrix.romSha256, kicks.target.sha256);
assert.equal(kickSide.romSha256, kicks.target.sha256);
assert.equal(kickNative.targetSha256, kicks.target.sha256);
assert.equal(kickStatic.targetSha256, kicks.target.sha256);
assert.equal(kickStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(kickStatic.preserved).every(Boolean));
const kickCode = Buffer.from((await readFile(resolve(root, 'src/gameplay/combos-v2/combos.hex'), 'utf8')).trim(), 'hex');
assert.equal(sha256(kickCode), kickStatic.codeSha256);
assert.equal(kickCode.length, kickStatic.decodedBytes);
const counterPreview = await json('evidence/combo-counter-preview-v1/validation.json');
assert.equal(counterPreview.counterIsInRom, false);
assert.equal(sha256(await readFile(resolve(root, counterPreview.videoPath))), counterPreview.videoSha256);
assert.deepEqual(counterPreview.cases.map(item => [item.case, item.maxDisplayedCounter]), [['Goku', 2], ['Vegeta', 2], ['Bloqueo', 0], ['Fallo', 0]]);
assert(counterPreview.cases.every(item => item.counterHiddenAtEnd));
const combos = await json('patches/combos-v1/manifest.json');
assert.equal(sha256(await readFile(resolve(root, combos.patch.path))), combos.patch.sha256);
const comboMatrix = await json('evidence/combos-v1/matrix.json');
const comboRegression = await json('evidence/combos-v1/side-regression.json');
const comboStatic = await json('evidence/combos-v1/static.json');
assert.equal(comboMatrix.romSha256, combos.target.sha256);
assert.equal(comboRegression.romSha256, combos.target.sha256);
assert.equal(comboStatic.targetSha256, combos.target.sha256);
assert(comboMatrix.passed && comboRegression.passed);
assert.equal(comboStatic.outsideAllowedChangedBytes, 0);
assert(Object.values(comboStatic.preserved).every(Boolean));
assert.equal(comboStatic.decodedInstructionBytes, comboStatic.codeBytes);
const comboCode = Buffer.from((await readFile(resolve(root, 'src/gameplay/combos-v1/combos.hex'), 'utf8')).replace(/\s/g, ''), 'hex');
assert.equal(comboCode.length, comboStatic.codeBytes);
assert.equal(sha256(comboCode), comboStatic.codeSha256);
const intro66 = await json('patches/review-v6-6/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro66.patch.path))), intro66.patch.sha256);
const native66 = await json('evidence/intro-original-lineup-v6-6/restoration.json');
assert.equal(native66.targetSha256, intro66.target.sha256);
assert(Object.values(native66.checks).every(Boolean));
assert(Object.values(native66.nativeChecks).every(Boolean));
const intro65 = await json('patches/review-v6-5/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro65.patch.path))), intro65.patch.sha256);
const native65 = await json('evidence/intro-refined-v6-5/validation.json');
assert.equal(native65.targetSha256, intro65.target.sha256);
assert(Object.values(native65.checks).every(Boolean));
assert(Object.values(native65.nativeBodyRGBErrorsPerCID).every(value => value === 0));
assert(native65.satMax.count <= 80 && native65.satMax.lineSprites <= 20 && native65.satMax.linePixels <= 320);
const intro64 = await json('patches/review-v6-4/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro64.patch.path))), intro64.patch.sha256);
const intro63 = await json('patches/review-v6-3/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro63.patch.path))), intro63.patch.sha256);
const restoration63 = await json('evidence/intro-original-v6-3/restoration.json');
assert.equal(restoration63.targetSha256, intro63.target.sha256);
assert(Object.values(restoration63.checks).every(value => value === true));
assert(Object.values(restoration63.nativeCaptureChecks).every(value => value === true));
const intro62 = await json('patches/review-v6-2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, intro62.patch.path))), intro62.patch.sha256);
const intro62Evidence = await json('evidence/intro-v2/combined-validation.json');
assert.equal(intro62Evidence.targetSha256, intro62.target.sha256);
assert(Object.values(intro62Evidence.checks).every(value => value === true));
const asm62 = await json('research/disassembly-es/mapa-mod-v6-2.json');
assert.equal(asm62.sha256, intro62.target.sha256);
const manifest = await json('patches/gameplay-v1/manifest.json');
for (const patch of Object.values(manifest.patches)) assert.equal(sha256(await readFile(resolve(root, patch.path))), patch.sha256, patch.path);
const hex = (await readFile(resolve(root, 'src/gameplay/v1/controls.hex'), 'utf8')).replace(/\s/g, '');
assert.match(hex, /^(?:[0-9a-f]{2})+$/);
const code = Buffer.from(hex, 'hex');
assert.equal(code.length, manifest.assembly.bytes);
assert.equal(sha256(code), manifest.assembly.sha256);
const graphics = await json('project/graphics.json');
const images = graphics.categories.flatMap(category => category.items);
assert.equal(images.length, 71);
assert.equal(images.length, graphics.imageCount);
assert.equal(new Set(images.map(item => item.path)).size, images.length);
for (const item of images) {
  assert(!item.path.includes('..') && !item.path.includes('\\'));
  assert.equal(sha256(await readFile(resolve(root, item.path))), item.sha256, item.path);
}
const decisions = await json('project/decisions.json');
assert.equal(decisions.presentation.selected, 'C anime cálido');
assert.equal(decisions.presentation.modCredit.text, '- 2026 ALEX LLAO');
assert.equal(decisions.presentation.modCredit.usePseudonym, false);
assert.equal(decisions.preservePreviousVersions, true);
assert.deepEqual(decisions.auras.lightningAllowedOnly, []);
await stat(resolve(root, decisions.presentation.image));
await stat(resolve(root, decisions.auras.image));
const matrix = await json('evidence/gameplay-v1/character-matrix.json');
assert.equal(matrix.length, 22);
assert.equal(new Set(matrix.map(item => `${item.mode}:${item.character_id}`)).size, 22);
assert(matrix.every(item => item.passed && Object.values(item.checks).every(Boolean)));
const summary = await json('evidence/gameplay-v1/summary.json');
assert.equal(summary.romSha256, manifest.targets.gameplay.sha256);
assert.equal(summary.damageMatchesOriginal, true);
assert.equal(summary.queuedHitInterruptions, 15);
const aura = await json('patches/auras-c2-v1/manifest.json');
assert.equal(aura.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, aura.patch.path))), aura.patch.sha256);
const readHex = async path => Buffer.from((await readFile(resolve(root, path), 'utf8')).replace(/\s/g, ''), 'hex');
assert.equal(sha256(await readHex(aura.code.assemblyHex)), aura.code.assembled_sha256);
assert.equal((await readHex(aura.tiles.hex)).length, 45 * 32);
const auraMaps = await readHex(aura.maps.hex);
assert.equal(aura.maps.addresses.length, 16);
for (const address of aura.maps.addresses) {
  const offset = Number(address) - Number(aura.maps.base);
  const count = auraMaps.readUInt16BE(offset);
  assert(count > 0 && count <= 34);
  for (let i = 0; i < count; i++) {
    const at = offset + 2 + i * 6;
    const tile = auraMaps.readUInt16BE(at) & 0x7ff;
    const size = auraMaps[at + 5];
    const tiles = (((size >> 2) & 3) + 1) * ((size & 3) + 1);
    assert(tile >= 0x513 && tile + tiles <= 0x540, 'Aura fuera del espacio de VRAM reservado');
  }
}
const auraValidation = await json('evidence/auras-c2-v1/validation.json');
assert.equal(auraValidation.target_sha256, aura.target.sha256);
assert.equal(auraValidation.characters.length, 11);
assert.deepEqual(auraValidation.characters.filter(item => item.lightning).map(item => item.character_id), [1, 5]);
for (const item of auraValidation.characters) {
  assert(item.exit_completed && item.movement_after_release && item.scratch_magic_stable);
  assert.equal(sha256(await readFile(resolve(root, 'assets/media/auras-c2-v1', item.video))), item.sha256);
}
const auraQa = await json('evidence/auras-c2-v1/runtime-qa.json');
assert.equal(auraQa.prototype_sha256, aura.target.sha256);
assert.equal(auraQa.frames_with_aura_when_both_phase_zero.length, 0);
assert.equal(auraQa.native118_11f_match_all_frames, true);
const aura2 = await json('patches/auras-c2-v2/manifest.json');
assert.equal(aura2.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, aura2.patch.path))), aura2.patch.sha256);
assert.equal(sha256(await readHex(aura2.code.assemblyHex)), aura2.code.assembled_sha256);
const tiles2 = await readHex(aura2.tiles.hex);
assert.equal(tiles2.length, 45 * 32);
assert.equal(sha256(tiles2), aura2.tiles.sha256);
const maps2 = await readHex(aura2.maps.hex);
assert.equal(sha256(maps2), aura2.maps.sha256);
assert.equal(aura2.maps.storage.length, 128);
for (const entry of aura2.maps.storage) {
  const count = maps2.readUInt16BE(entry.offset);
  assert(count > 0 && count <= 50);
  assert.equal(entry.bytes, 2 + count * 6);
  for (let i = 0; i < count; i++) {
    const at = entry.offset + 2 + i * 6;
    const tile = maps2.readUInt16BE(at) & 0x7ff, size = maps2[at + 5];
    assert(tile >= 0x513 && tile + (((size >> 2) & 3) + 1) * ((size & 3) + 1) <= 0x540);
  }
}
const validation2 = await json('evidence/auras-c2-v2/validation.json');
assert.equal(validation2.target_sha256, aura2.target.sha256);
assert.deepEqual(validation2.flame_sizes.c2_v2, [80, 128]);
assert.equal(validation2.characters.length, 11);
assert.deepEqual(validation2.characters.filter(item => item.lightning).map(item => item.character_id), [1, 5]);
for (const item of validation2.characters) {
  assert(item.exit_completed && item.movement_after_release && item.scratch_magic_stable);
  assert.equal(sha256(await readFile(resolve(root, 'assets/media/auras-c2-v2', item.video))), item.sha256);
}
assert.equal(validation2.graphics_budgets.length, 11);
assert(validation2.graphics_budgets.every(item => item.sprites <= 80 && item.scanline <= 20 && item.pixels <= 320));
const qa2 = await json('evidence/auras-c2-v2/runtime-qa.json');
assert.equal(qa2.sha256, aura2.target.sha256);
assert.equal(qa2.tested.natural_collisions, 6);
assert.equal(qa2.tested.residual_sprites_when_both_phases_zero, 0);
assert(qa2.capacity.tested_max_sprites_per_frame <= 80);
assert(qa2.capacity.tested_max_scanline_sprites <= 20);
assert(qa2.capacity.tested_max_scanline_width_pixels <= 320);
await verifyAuraV3(root, manifest.source.sha256);
await verifyAuraV4(root, manifest.source.sha256);
const noRays = await json('patches/auras-c2-v3-no-rays/manifest.json');
assert.equal(noRays.source.sha256, manifest.source.sha256);
assert.equal(sha256(await readFile(resolve(root, noRays.patch.path))), noRays.patch.sha256);
assert.deepEqual(noRays.lightningCharacterIds, []);
const noRaysTable = await readHex(noRays.mapTable.hex);
assert.equal(noRaysTable.length, 384 * 4);
const v3 = await json('patches/auras-c2-v3/manifest.json');
const v3maps = await readHex(v3.maps.hex);
for (let i = 0; i < 384; i++) {
  const plain = i - (i % 8 >= 4 ? 4 : 0);
  assert.equal(noRaysTable.readUInt32BE(i * 4), Number(v3.maps.pointers[plain]));
  const entry = v3.maps.storage.find(e => Number(e.address) === noRaysTable.readUInt32BE(i * 4));
  assert(entry);
  const count = v3maps.readUInt16BE(entry.offset);
  for (let j = 0; j < count; j++) {
    const tile = v3maps.readUInt16BE(entry.offset + 2 + j * 6) & 0x7ff;
    assert(tile < 0x54b || tile > 0x550, 'Un mapa alcanzable conserva rayos');
  }
}

const reviewV2 = await json('patches/review-v2/manifest.json');
assert.equal(sha256(await readFile(resolve(root, reviewV2.patch.path))), reviewV2.patch.sha256);
const reviewCode = await readHex(reviewV2.assembly.path);
assert.equal(reviewCode.length, reviewV2.assembly.bytes);
assert.equal(sha256(reviewCode), reviewV2.assembly.sha256);
const reviewMatrix = await json('evidence/gameplay-v2/movement-matrix.json');
assert.equal(reviewMatrix.length, 22);
assert(reviewMatrix.every(item => item.passed && Object.values(item.checks).every(Boolean)));
for (const name of ['final-p1', 'final-p2-turbo']) {
  assert.equal((await json(`evidence/gameplay-v2/${name}.json`)).rom, reviewV2.target.sha256);
}

const reviewV3 = await json('patches/review-v3/manifest.json');
assert.equal(sha256(await readFile(resolve(root, reviewV3.patch.path))), reviewV3.patch.sha256);
for (const entry of Object.values(reviewV3.code)) {
  const bytes = await readHex(entry.path);
  assert.equal(bytes.length, entry.bytes);
  assert.equal(sha256(bytes), entry.sha256);
}
const sideMatrix = await json('evidence/side-switch/matrix.json');
assert.equal(sideMatrix.romSha256, reviewV3.target.sha256);
assert.equal(sideMatrix.jobs, 22);
assert.equal(sideMatrix.cases, 374);
assert(sideMatrix.passed && sideMatrix.failures.length === 0);
assert(sideMatrix.results.every(job => job.cases.every(item => item.passed && Object.values(item.checks).every(Boolean))));
const sideStatic = await json('evidence/side-switch/static-verification.json');
assert.equal(sideStatic.targetSha256, reviewV3.target.sha256);
assert(sideStatic.onlyAllowedRangesChanged && Object.values(sideStatic.preserved).every(item => item.unchanged));

const introReview = await json('patches/review-v6-1/manifest.json');
assert.equal(introReview.baseReviewSha256, reviewV3.target.sha256);
assert.equal(sha256(await readFile(resolve(root, introReview.patch.path))), introReview.patch.sha256);
const introValidation = await json('evidence/intro-v1/validation.json');
assert.equal(introValidation.targetSha256, introReview.target.sha256);
assert(Object.values(introValidation.checks).every(Boolean));
for (const capture of introValidation.captures) {
  assert.equal(sha256(await readFile(resolve(root, capture.path))), capture.sha256);
}

async function walk(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (['.git', 'node_modules', '.build', 'build-local', 'dist'].includes(entry.name)) continue;
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(path));
    else files.push(path);
  }
  return files;
}
const files = await walk(root);
for (const path of files.filter(path => extname(path) === '.md')) {
  const text = await readFile(path, 'utf8');
  for (const match of text.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
    const link = match[1].split('#')[0];
    if (!link || /^(https?:|mailto:)/.test(link)) continue;
    await stat(resolve(dirname(path), decodeURIComponent(link)));
  }
}
let tracked = [];
try { tracked = execFileSync('git', ['ls-files', '-z'], { cwd: root, encoding: 'utf8' }).split('\0').filter(Boolean); }
catch { /* An exported source archive may have no .git metadata. */ }
for (const path of tracked) {
  assert(!/\.(bin|smd|gen|zip|dll|exe|state|srm)$/i.test(path), `Archivo generado/base inesperado en Git: ${path}`);
}
console.log(`Verificado: ${images.length} imágenes, Goku cálido con reparto original, ${matrix.length} combinaciones históricas, parches, código y enlaces locales (${files.length} archivos).`);
