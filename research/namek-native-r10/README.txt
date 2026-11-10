R10 native resource corrections. Run from project root with the existing R6/R9 working pipeline and original user ROM.
No ROM or video is included. build.py imports R9 resources and existing house/cloud artwork.
build.py -> integrate.py -> fresh prepare-scenes.py -> record.py for each variant -> verify-runtime.py -> verify-build.py -> package.py -> fix-detail-qa.py.
Use a fresh, consistent state folder after any changed ROM. Final evidence uses states-final-r10b.
Changes are native graphics only; no new generated artwork, gameplay modifications, VDP sprite animation or postproduction background replacement.
