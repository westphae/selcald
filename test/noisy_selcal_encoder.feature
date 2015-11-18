# Created by eric at 11/13/15
Feature: SELCAL tones for a variety of codes can be encoded with varying noise
  levels, varying tone accuracies, and varying tone and pause lengths, all
  within the SELCAL specifications.  Incorrect SELCAL-like signals can also be
  generated.  Noise can be added to the signal and the signal distorted (within
  SELCAL specifications).

  Scenario Outline: Tones not in the SELCAL spectrum can be generated.
    Given the frequency <freq> and a duration <dur>
    When the tone generation function is run
    Then a sample is generated for that frequency <freq>
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | freq    | dur |
      | 315.9   | 1   |
      | 946.3   | 0.5 |
      | 1565.6  | 2.5 |

  Scenario Outline: Each tone in the SELCAL spectrum can be generated.
    Given the SELCAL tone <tone>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequency <freq>
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | tone | freq   |
      | A    | 312.6  |
      | B    | 346.7  |
      | C    | 384.6  |
      | D    | 426.6  |
      | E    | 473.2  |
      | F    | 524.8  |
      | G    | 582.1  |
      | H    | 645.7  |
      | J    | 716.1  |
      | K    | 794.3  |
      | L    | 881.0  |
      | M    | 977.2  |
      | P    | 1083.9 |
      | Q    | 1202.3 |
      | R    | 1333.5 |
      | S    | 1479.1 |

  Scenario Outline: Two simultaneous SELCAL tones can be generated,
  corresponding to the first syllable of a SELCAL message.
    Given the SELCAL tones <tones>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | tones |
      | AB    |
      | CH    |
      | DR    |
      | LR    |

  Scenario Outline: A full SELCAL signal can be generated.
    Given the SELCAL tones <tones>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | tones |
      | ASBK  |
      | DQJR  |
      | FMBG  |
      | FMHQ  |
      | FPQR  |
      | GJMR  |
      | JPAM  |
      | LPCG  |
      | LPHQ  |
      | MPEQ  |
      | PQCG  |
      | PRFJ  |
      | PRGQ  |

  Scenario Outline: A full SELCAL signal can be generated with background noise.
    Given the SELCAL tones <tones>
    And a chosen noise level <noise_level>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | tones | noise_level |
      | ASBK  | 0.2         |
      | DQJR  | 1.1         |
      | FMBG  | 0.3         |
      | FMHQ  | 0.8         |
      | FPQR  | 4.6         |
      | GJMR  | 0.8         |
      | JPAM  | 0.9         |
      | LPCG  | 9.7         |
      | LPHQ  | 0.8         |
      | MPEQ  | 0.0         |
      | PQCG  | 1.0         |
      | PRFJ  | 0.4         |
      | PRGQ  | 2.5         |

  Scenario Outline: A full SELCAL signal can be generated with background noise and variations.
    Given the SELCAL tones <tones>
    And a chosen noise level <noise_level>
    And a choice of <randomization>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, makes the correct sound.

    Examples:
      | tones | noise_level | randomization |
      | ASBK  | 0.2         | True          |
      | DQJR  | 1.1         | True          |
      | FMBG  | 0.3         | True          |
      | FMHQ  | 0.8         | True          |
      | FPQR  | 4.6         | True          |
      | GJMR  | 0.8         | True          |
      | JPAM  | 0.9         | True          |
      | LPCG  | 9.7         | True          |
      | LPHQ  | 0.8         | True          |
      | MPEQ  | 0.0         | True          |
      | PQCG  | 1.0         | True          |
      | PRFJ  | 0.4         | True          |
      | PRGQ  | 2.5         | True          |
