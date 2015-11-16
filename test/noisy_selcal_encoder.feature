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
    And when fed to an audio generation library, sounds the correct frequency.

    Examples:
      | freq    | dur |
      | 315.9   | 1   |
      | 946.3   | 0.5 |
      | 1565.6  | 2.5 |

  Scenario Outline: Each tone in the SELCAL spectrum can be generated.
    Given the SELCAL tone <tone>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequency <freq>
    And when fed to an audio generation library, sounds the correct frequency.

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
     And when fed to an audio generation library, sounds the correct frequencies.

     Examples:
       | tones |
       | AB    |
       | CH    |
       | DR    |
       | LR    |

  Scenario Outline: A full SELCAL signal can be generated.
    Given the SELCAL tones <tone1> <tone2> <tone3> <tone4>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, sounds the correct frequencies.

    Examples:
      | tone1 | tone2 | tone3 | tone4 |
      | A     | B     | F     | M     |
      | C     | H     | G     | S     |
      | D     | R     | L     | N     |

  Scenario: Background noise can be generated.
    Given a noise level
    When the tone generation function is run
    Then a sample is generated for the corresponding noise
    And when fed to an audio generation library, sounds the correct noise.

  Scenario Outline: A full SELCAL signal can be generated with background noise.
    Given the SELCAL tones <tone1> <tone2> <tone3> <tone4>
    And a chosen noise level <noise_level>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, sounds the correct frequencies
    And there is appropriate background noise.

    Examples:
      | tone1 | tone2 | tone3 | tone4 | noise_level |
      | A     | B     | F     | M     | 0.0         |
      | A     | B     | F     | M     | 0.2         |
      | C     | H     | G     | S     | 0.4         |
      | C     | H     | G     | S     | 0.6         |
      | D     | R     | L     | N     | 0.8         |
      | D     | R     | L     | N     | 1.0         |

  Scenario Outline: A full SELCAL signal can be generated with background noise and
    variations of the tone frequencies and durations and the pause duration
    consistent with the SELCAL standard.
    Given the SELCAL tones <tone1> <tone2> <tone3> <tone4>
    And a chosen noise level <noise_level>
    When the tone generation function is run
    Then a sample is generated for the corresponding frequencies
    And when fed to an audio generation library, sounds the correct frequencies
    And there is appropriate background noise.

    Examples:
      | tone1 | tone2 | tone3 | tone4 | noise_level |
      | A     | B     | F     | M     | 0.0         |
      | A     | B     | F     | M     | 0.2         |
      | C     | H     | G     | S     | 0.4         |
      | C     | H     | G     | S     | 0.6         |
      | D     | R     | L     | N     | 0.8         |
      | D     | R     | L     | N     | 1.0         |
