from pathlib import Path
import json
root=Path('work/intro-characters');plan=json.loads((root/'material-plan.json').read_text());mapping=plan['targetMapping'];pal={int(k):v for k,v in plan['battle_palette_words'].items()}
usage=json.loads((root/'extracted/extraction.json').read_text())['characterIndexUsage']
owner=(root/'extracted/pixel-owner-cid-plus-one.bin').read_bytes();bank=(root/'extracted/pixel-bank.bin').read_bytes();idx=(root/'extracted/pixel-index.bin').read_bytes()
protected={(r['cid'],key)for r in plan['protected_three_shade_material_ramps']for key in r['source']}
specs=[
 ('a18_warm_gray_trim_to_light_gray',6,['2:13'],15,'Warmgraytrim0664 becomes existinglightgray0AAA; secondaryboot/clothestrim, notdenim/skin/hair.'),
 ('gohan_gray_trim_to_white',1,['1:12'],15,'Tinygraytrim0AAA becomes existingwhite0EEE; violetcloththree shades untouched.'),
 ('ginyu_armor_light_gray_to_white',10,['1:10'],15,'Lightarmorgray0AAA mergeswhite0EEE; violetskin0846/A68/CAChasnochanges.'),
 ('recoome_blue_black_outline_to_neutral_black',9,['2:9'],10,'Verydarkblue0200 outline becomes actualnonzero0222 black; copperhair/skinramps unchanged.'),
 ('recoome_armor_mid_gray_to_light_gray',9,['2:13'],14,'Armorgray0888 mergesexisting0AAA lightgray, retainingblack/darkgray/white.'),
 ('recoome_copper_trim_to_copper_highlight',9,['2:8'],11,'Brown-orange0248 trim becomes existingcopper026A highlight; protectedhairsource2:1/6/2 unchanged.'),
 ('freezer_outline_to_dark_violet',8,['2:10'],4,'Darkred0006 outline becomes approveddarkviolet0622 surroundingwhite/violetbody. No change tothreewhiteorvioletprotectedramps.'),
 ('freezer_secondary_plate_shadow_to_violet_mid',8,['2:12'],5,'Secondaryplate0622 shadow merges0826 mid; protectedvioletshadow2:9remains0622.'),
 ('cell_violet_trim_shadow_to_violet_mid',5,['3:10'],11,'Violettrim0646 merges0846, leavinggreen0240/0486/06CAtriplet intact.'),
 ('vegeta_armor_gray_shadow_to_gray_mid',3,['3:9'],8,'Secondaryarmor0666 shadow merges0AAA mid, retaining0AAA/0CCC/0EEE values; suitandhumanskin untouched.'),
 ('vegeta_armor_gray_mid_to_gray_light',3,['3:8'],14,'Secondaryarmor0AAA mid merges0CCC light; alternative/additionalneutralramp simplification.'),
 ('vegeta_small_warm_armor_trim_shade',3,['3:13'],7,'Tinywarmarmor0468 trim mergesexisting0246 warmshadow; no navyorhumanhead change.'),
 ('trunks_pants_gray_mid_to_gray_dark',4,['2:13'],10,'Pantsgray0666 merges0444, retainingblack/pantswhite; bluejacket0642/0A86 unchanged.'),
 ('trunks_boot_dark_warm_shade_to_shared_warm_shade',4,['2:1'],7,'Bootshadow0224 becomes actual0246 warmbrown; a slightlylightersharedwarmshade, notunrelatedblueorviolet.'),
 ('piccolo_black_outline_to_charcoal',2,['1:14'],13,'Index0black0000 istransparentinbattlepalette, notanopaquevisiblebattleindex. Useactualnonzerocharcoal0444 alreadyusedfortrim; greens/purple/pinkprotectedramps untouched.'),
 ('gohan_black_outline_to_native_dark_maroon',1,['1:14','2:10'],9,'Index0black0000 isnotvisiblebattlecolorproof. Useexistingnonzero0026 nativeverydarkwarmoutline/beltshade; clothandhumanskin unaffected.'),
 ('piccolo_tiny_white_to_light_gray',2,['1:15'],14,'Fivevisiblewhitepixels0CCC becomeapprovedlightgray0AAA; secondaryhighlight, notmainmaterial.'),
 ('piccolo_tiny_gray_trim_to_light_gray',2,['1:12'],14,'Tinygraytrim0444 becomes0AAA matchingtheoptionalneutralhighlight. Green/purple/pinktriplets unchanged.'),
 ('ginyu_armor_gray_to_light_gray',10,['1:12'],10,'Armor0666 shadow merges0AAA lightgray, retainingoutlineandwhite. Largearmorflatness tradeoff, notvioletskin.'),
 ('ginyu_armor_gray_to_white',10,['1:12'],15,'Alternative strongerarmor666->EEE merge. Combinewitharmorlightgray->whiteonlyasexplicitflatwhitearmortradeoff; skinthree shades preserved.'),
 ('trunks_gray_pants_to_dark',4,['2:12','2:13'],4,'Alternative strongerpantsmerge0444/0666->0222 darktrousers. Bluejacketandhumanhead unaffected; pantslosegrayhighlights.'),
 ('vegeta_armor_light_grays_to_white',3,['3:7','3:8'],15,'SecondaryCCC/AAA armorlights becomeEEE, retainingdarkerarmorgrayandallnavy/headcolors.'),
 ('recoome_armor_dark_gray_to_black',9,['2:12'],10,'Secondary444 armorline becomes222, retainingarmorwhite/lightgray andprotectedskin/copperhair.'),
 ('recoome_armor_light_grays_to_white',9,['2:13','2:14'],15,'Secondary888/AAA armorlights becomeEEE, retaining444 shadowand222outline; skin/copperhair untouched.'),
 ('gohan_secondary_whites_to_warm_white',1,['1:12','1:15'],3,'Tinygraytrim/eye highlights becomeapprovedwarmwhiteAEE. Thiswordalreadyusedinhumanhead; violetclothandactualskintriplet unchanged.'),
 ('cell_secondary_gray_to_darker_gray',5,['3:7'],8,'Secondary666 gray becomes444 charcoal, retaininggreenandpurplematerials.'),
 ('a18_secondary_gray_trim_to_white',6,['2:12','2:13'],11,'SecondaryAAA/0664 boot/garmenttrim becomesapprovedEEE white, keepingallskin/hair/denimtargets unchanged.')]
candidates=[]
for name,cid,keys,palindex,why in specs:
 assert not any((cid,k)in protected for k in keys),(name,keys)
 changes=[];visible=0;units=0
 for key in keys:
  srcbank,srcidx=map(int,key.split(':'));n=sum(o==cid+1 and p==srcbank and i==srcidx for o,p,i in zip(owner,bank,idx));u=usage[str(cid)][key]
  changes.append({'source_key':key,'from_word':mapping[str(cid)][key],'to_word':pal[cid][palindex],'approved_battle_index':palindex,'visible_pixels':n,'native_unit_pixels_including_occlusion':u});visible+=n;units+=u
 candidates.append({'id':name,'cid':cid,'changes':changes,'visible_changed_pixels':visible,'unit_changed_pixels':units,'reason':why,'protected_source_keys_changed':0,'semantics':'Apply perlistedsourcekey only; never replace everyoccurrenceofoldword in aCID, because otherkeys may be protected material.'})
out={'status':'Legal optional same-CID approved-palette secondaryshade merges for exact-packing subset search; no ROM edits','source_plan':'work/intro-characters/material-plan.json','mapping_base':'work/intro-characters/target-mapping.json','protected':'All13protectedtriplets unchanged byEVERY candidate, additionally human skinandhair corematerialtargets unaffected.','candidates':candidates,'method':'Manualmaterialroles and samehue/neutralshade merges; no RGBnearest. Countsfromexactownerpixelbuffersandnativeunitindexusage. Visiblecounts countbeforeproposal, candidateoverlap/combinationstotal mustbecomputedonresultmapping ratherthansumming blindly.','priority':'Try lowvisiblecounts andglobalcolor-removal first, then pergroupgrayreductions; comparepackednativepreview beforetakinghighercoverageCellviolettrim orlargepants merges.','special_note':'Blackword0000 fromCIDpaletteindex0wasallowedbyfirstpassbutisnotactuallyvisiblebattlecolor evidence. Piccolocharcoal/Gohanmaroon substitutions are moredefensible nonzeroindexcolors; Krillin0000hasactualnonzeroindex14andisvalid.','limits':'These are authorized proposedsecondarymaterialtradeoffs, notuserapproval. MappingbyCIDsourceindexcannotdistinguish twomaterials sharingoneoldindex; renderandreview affectedparts. PreservefaceGfixed.'}
(root/'merge-candidates.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps([{'id':c['id'],'visible':c['visible_changed_pixels'],'units':c['unit_changed_pixels']}for c in candidates],indent=2))
