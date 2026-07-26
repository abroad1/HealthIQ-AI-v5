# Historic waist unitless impact assessment

**Work:** ARCH-CONV-CORRECT-1 closure stabilisation (non-mutating audit)
**Generated:** 2026-07-26
**Scope:** Read-only classification of persisted bare waist_circumference values.

## Evidence boundary

- Former FE displayed unitless "Waist circumference" and stored bare numbers.
- Database scan found bare numbers only (no historic unit-labelled dicts).
- Cluster ~75–93 is consistent with UK centimetre entry.
- No stored value of 166.
- Incorrect mapped value below = former inches×2.54 mishandling (pre-fix).
- Remediation (stale mark / regenerate) is separately authorised; this report does not mutate rows.

## Summary counts

- legacy bare rows classified: **48**
- used_incorrectly: **12**
- dropped_as_implausible: **36**
- analysis_start_blocked: **0**

## Classification table

| analysis_id | created_at | original_value | incorrect_mapped_cm_if_inches | likely_outcome |
|---|---|---:|---:|---|
| 50e40d14-07f2-42bd-aea7-b0677cd543e0 | 2026-04-12 08:18:36.956552 | 93 | 236.22 | dropped_as_implausible |
| 95066185-004c-4826-b74b-df7072d70c08 | 2026-04-12 15:45:51.498920 | 91 | 231.14 | dropped_as_implausible |
| 1322e1b8-7b84-4186-a03c-ec9a785b805f | 2026-04-18 07:38:59.893624 | 92 | 233.68 | dropped_as_implausible |
| 6f702428-ec3e-4e00-9416-280904e9d4b3 | 2026-04-23 18:17:45.681040 | 93 | 236.22 | dropped_as_implausible |
| ff08b1f9-f9d1-4acd-9b94-8bfd4c60df67 | 2026-04-25 11:36:56.698905 | 92 | 233.68 | dropped_as_implausible |
| e5cfbc62-93fa-4bac-8894-dcb69117ac4c | 2026-04-25 21:23:55.250977 | 77 | 195.58 | used_incorrectly |
| c1c061ab-4691-4a47-80b8-2938ae1460e4 | 2026-04-26 16:46:45.839413 | 90 | 228.6 | dropped_as_implausible |
| 02df9062-eba8-4df1-8072-8d2182aca35d | 2026-04-27 17:38:36.874452 | 77 | 195.58 | used_incorrectly |
| 7fc35b86-15c2-4d76-843a-e964263be0b7 | 2026-04-28 15:47:57.486470 | 77 | 195.58 | used_incorrectly |
| a3244490-dd74-4922-a1c6-49a25c1f6604 | 2026-04-28 16:55:54.174297 | 60 | 152.4 | used_incorrectly |
| 7f780514-d288-4331-8020-8866744b70ae | 2026-04-28 17:42:57.302704 | 67 | 170.18 | used_incorrectly |
| ad721d67-f2e8-4942-8450-8598b8e35343 | 2026-05-02 08:27:35.201627 | 75 | 190.5 | used_incorrectly |
| ecb519ad-4d22-44a6-bae3-75d652c761f7 | 2026-05-12 11:29:35.473753 | 92 | 233.68 | dropped_as_implausible |
| b2dfa0c4-efd6-467f-9f2a-84bdf20d8d51 | 2026-05-12 21:07:42.137656 | 91 | 231.14 | dropped_as_implausible |
| 782b889f-69f8-44de-ad18-d9688f6b5c16 | 2026-05-13 18:23:17.454069 | 91 | 231.14 | dropped_as_implausible |
| bfbd8896-e5ab-4a63-9169-89c26efb67ca | 2026-05-14 20:50:31.336288 | 91 | 231.14 | dropped_as_implausible |
| e4dc8e59-2588-4943-b37b-a299c89f9442 | 2026-05-16 12:54:37.090538 | 89 | 226.06 | dropped_as_implausible |
| ac253c67-2489-4c1e-9ed7-b033f3e55abd | 2026-05-16 13:20:46.343971 | 88 | 223.52 | dropped_as_implausible |
| bd17f7b4-74af-4668-9d25-e6bfdbbd957c | 2026-05-16 13:24:20.937323 | 89 | 226.06 | dropped_as_implausible |
| a817efa9-f915-4309-8b25-51c44cf98d62 | 2026-05-16 19:43:31.207393 | 79 | 200.66 | dropped_as_implausible |
| 7cc8b2d5-c8f0-4138-ba18-8540eece06a1 | 2026-05-17 10:04:35.466853 | 78 | 198.12 | used_incorrectly |
| b24ce358-02e3-4058-a667-34328a4168a2 | 2026-05-17 10:07:37.525691 | 80 | 203.2 | dropped_as_implausible |
| 91046b62-114f-44a3-a2ab-2b885ea5782b | 2026-05-17 11:18:39.186429 | 78 | 198.12 | used_incorrectly |
| 28a29114-6621-487b-b671-52f921cf4a5c | 2026-05-17 11:37:07.528759 | 80 | 203.2 | dropped_as_implausible |
| 7b8c58b5-191f-41e7-8fe4-a66938bb0a98 | 2026-05-17 11:48:34.624050 | 78 | 198.12 | used_incorrectly |
| c440dfa2-12a1-4e29-95a5-ee07a2397c59 | 2026-05-17 12:56:29.518512 | 89 | 226.06 | dropped_as_implausible |
| e3a1ee79-963e-46a1-afee-58657d1ffb55 | 2026-05-17 17:04:26.290169 | 78 | 198.12 | used_incorrectly |
| 7aacc734-95cf-4ea5-a19c-0d03d98dd2e9 | 2026-05-24 06:55:24.044068 | 76 | 193.04 | used_incorrectly |
| f2dcb58f-e816-4ff6-9011-e93c5d48b82c | 2026-05-24 21:07:46.901514 | 83 | 210.82 | dropped_as_implausible |
| d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579 | 2026-05-24 22:28:21.756337 | 88 | 223.52 | dropped_as_implausible |
| 3c4d2b1c-7802-4174-ad49-2ff9a09c8727 | 2026-05-25 09:34:08.275739 | 79 | 200.66 | dropped_as_implausible |
| d7417288-7e11-48da-8716-d0f63f77c491 | 2026-05-26 17:23:37.527400 | 22 | 55.88 | used_incorrectly |
| 1aa91295-dafb-4ac6-96ae-6b38dadb7fb9 | 2026-05-26 19:43:03.965377 | 9 | 22.86 | dropped_as_implausible |
| bb695d3c-453e-4e49-abff-ae80587b4248 | 2026-05-27 17:34:55.092919 | 89 | 226.06 | dropped_as_implausible |
| 18e14232-9f93-45e6-820c-004ab5a16235 | 2026-05-30 10:55:22.604997 | 83 | 210.82 | dropped_as_implausible |
| 746f2b0a-b470-4d87-8ed8-e2c3d1e68c02 | 2026-05-30 11:42:43.348323 | 86 | 218.44 | dropped_as_implausible |
| 26dfe337-3b45-4837-8169-0d74d63e0fbc | 2026-05-30 22:04:12.029300 | 82 | 208.28 | dropped_as_implausible |
| f26e6371-6df6-4ac6-a189-b4967f0f3f98 | 2026-05-31 09:02:03.143607 | 84 | 213.36 | dropped_as_implausible |
| f0e5e6ff-4952-44a2-b144-1cc35344c2d2 | 2026-05-31 09:41:36.602459 | 86 | 218.44 | dropped_as_implausible |
| 99cdc548-d312-446a-8c68-f20d47ba5b76 | 2026-05-31 09:44:29.462079 | 86 | 218.44 | dropped_as_implausible |
| 70601969-87e1-4968-b0f8-3dfee55d9472 | 2026-05-31 10:27:49.193057 | 86 | 218.44 | dropped_as_implausible |
| ea11d98b-ebe2-442e-abd2-60a591f36a9e | 2026-05-31 10:42:59.131625 | 86 | 218.44 | dropped_as_implausible |
| 33e5519a-25cc-410e-b5fc-ce5830153bf2 | 2026-05-31 10:52:28.906467 | 86 | 218.44 | dropped_as_implausible |
| fdf9bc74-70db-4d36-be8a-8c709c654df8 | 2026-06-16 16:29:24.620405 | 84 | 213.36 | dropped_as_implausible |
| 6bcbf1de-d97f-4a1c-9556-e3a6e0625fd1 | 2026-06-16 20:29:10.139290 | 83 | 210.82 | dropped_as_implausible |
| 8501fe0a-1e8b-401e-9650-f2c79e5d7d13 | 2026-06-17 16:56:23.529270 | 84 | 213.36 | dropped_as_implausible |
| b14db78b-1198-414c-bcea-6c0ee9e0bdc6 | 2026-06-20 07:30:17.440701 | 79 | 200.66 | dropped_as_implausible |
| e34aaedf-b09f-42f0-8cc8-4653a00b4c10 | 2026-07-26 12:52:21.480717 | 90 | 228.6 | dropped_as_implausible |

## Data-remediation recommendation

1. Mark affected analyses stale / incompatible when a waist-unit policy id is introduced (separate change).
2. Prefer regenerate-with-latest after questionnaire re-entry with explicit cm/inches, or a governed one-off remap of legacy bare→cm for rows classified here.
3. Do not silently rewrite without audit trail.
