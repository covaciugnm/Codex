# Răspunsul autorului la auditul Apple R1

Autor: doctoral_apple_perception. Data: 2026-10-02. Domeniu: corecții proprii în capitolele 03, 04 și 05. Verdictul auditorului R1 și registrul constatărilor nu au fost modificate de autor; închiderea rămâne responsabilitatea auditului independent R2.

## APP-A01 — remediere propusă pentru verificare

- Capitolul 03 §3.6 separă session_id, map_epoch și clock_epoch. session_epoch este doar alias local pentru tripletul acestora.
- Capitolul 05 §5.4 definește adaptorul canonic: observation_id/sequence pentru observație, frame_id numai reper geometric, calibration_id imutabil pentru revizia calibrării, model_version pentru versiunea modelului, map_revision în interiorul map_epoch.
- Capitolul 04 §4.6 adoptă states observed/predicted/occluded/lost/retired, cu ambiguity_status ortogonal none/pose/identity/both. Eticheta ambiguous rămâne de interfață; archived se traduce retired numai pentru retragere explicită din inventar.
- APP-IF-01…05 definesc probe pentru restart, resetare spațială, salt de ceas, reordonare între fluxuri și conversie fără pierderi a ambiguității.
- Autorul roboticii a fost informat și aliniază propriul contract; nu i-am modificat fișierele.

## APP-A02 — remediere propusă pentru verificare

Capitolul 04 §4.5 fixează perturbația dreaptă T=That Exp(delta_xi), vectorul [rho,phi] exprimat în reperul obiectului, blocurile m²/rad²/m·rad, biasul separat și conversia prin adjoint către perturbarea stângă. Adaptorul către pose ROS declară explicit eroare de poziție aditivă și rotație infinitezimală fixed-axis în reperul extern, cu J=diag(R,R). Acest profil este delimitat de diferențele finite de unghiuri Euler și de covarianța Lie-left.

Informația necunoscută este marcată unavailable, nu matrice de zero. Termenii de corelație sunt păstrați ori aproximați conservator justificat. PER-07 definește verificare prin diferențe finite/eșantionare, conversie tur-retur, simetrie și semidefinire pozitivă, plus cazul observațiilor perfect corelate.

## Limite

Am revizuit specificația; nu am implementat sau executat APP-IF/PER-07, SDK Swift ori ROS. Solicit re-auditul independent al corecțiilor și al concordanței contractului actualizat. Nu declar acceptare în numele auditorului.
