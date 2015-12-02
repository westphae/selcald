# Created by eric at 11/13/15
Feature: Goertzel filter can accurately detect a selcal signal and report the code.

  Scenario Outline: Goertzel filter can detect a single SELCAL tone without noise.
    Given the SELCAL tone <tone>
    And a Goertzel filter tuned for tone <ftone>
    When the tone generation function is run without variations
    Then a sample is generated for the corresponding frequency
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does detect the frequencies.

    Examples:
      | tone | ftone  |
      | A    | A      |
      | B    | B      |
      | C    | C      |
      | D    | D      |
      | E    | E      |
      | F    | F      |
      | G    | G      |
      | H    | H      |
      | J    | J      |
      | K    | K      |
      | L    | L      |
      | M    | M      |
      | P    | P      |
      | Q    | Q      |
      | R    | R      |
      | S    | S      |

  Scenario Outline: Goertzel filter tuned for the wrong frequency does not detect
    a single SELCAL tone without noise.
    Given the SELCAL tone <tone>
    And a Goertzel filter tuned for tone <ftone>
    When the tone generation function is run without variations
    Then a sample is generated for the corresponding frequency
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does not detect the frequencies.

    Examples:
      | tone | ftone  |
      | A    | B      |
      | B    | C      |
      | C    | D      |
      | D    | E      |
      | E    | F      |
      | F    | G      |
      | G    | H      |
      | H    | J      |
      | J    | K      |
      | K    | L      |
      | L    | M      |
      | M    | P      |
      | P    | Q      |
      | Q    | R      |
      | R    | S      |
      | S    | B      |

  Scenario Outline: Goertzel filter does not detect a SELCAL tone in pure noise.
    Given a noise level <noise_level>
    And a Goertzel filter tuned for tone <ftone>
    When the tone generation function is run without variations
    Then a sample is generated
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does not detect the frequencies.

    Examples:
      | ftone | noise_level |
      | A     | 0.20        |
      | B     | 0.10        |
      | C     | 0.30        |
      | D     | 0.40        |
      | E     | 0.60        |
      | F     | 0.80        |
      | G     | 1.00        |
      | H     | 1.33        |
      | J     | 1.66        |
      | K     | 2.00        |
      | L     | 2.50        |
      | M     | 3.00        |
      | P     | 4.00        |
      | Q     | 5.00        |
      | R     | 7.00        |
      | S     | 9.99        |

  Scenario Outline: Goertzel filter can detect a single SELCAL tone with noise.
    Given the SELCAL tone <tone>
    And a chosen noise level <noise_level>
    And a Goertzel filter tuned for tone <ftone>
    When the tone generation function is run without variations
    Then a sample is generated for the corresponding frequency
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does detect the frequencies.

    Examples:
      | tone | ftone  | noise_level |
      | A    | A      | 0.20        |
      | B    | B      | 2.60        |
      | C    | C      | 0.90        |
      | D    | D      | 3.10        |
      | E    | E      | 1.20        |
      | F    | F      | 5.30        |
      | G    | G      | 1.40        |
      | H    | H      | 0.80        |
      | J    | J      | 9.20        |
      | K    | K      | 3.50        |
      | L    | L      | 5.90        |
      | M    | M      | 7.30        |
      | P    | P      | 0.10        |
      | Q    | Q      | 2.40        |
      | R    | R      | 1.60        |
      | S    | S      | 3.70        |

  Scenario Outline: Goertzel filter can detect two SELCAL tones without noise.
    Given the SELCAL tones <tones>
    And a Goertzel filter tuned for tones <ftones>
    When the tone generation function is run without variations
    Then a sample is generated for the corresponding frequency
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does detect the frequencies.

    Examples:
      | tones | ftones |
      | AC    | AC     |
      | BH    | BH     |
      | CK    | CK     |
      | DE    | DE     |
      | EG    | EG     |
      | FP    | FP     |
      | GR    | GR     |
      | HM    | HM     |
      | JQ    | JQ     |
      | KL    | KL     |
      | LS    | LS     |
      | BM    | BM     |
      | DP    | DP     |
      | AQ    | AQ     |
      | FR    | FR     |
      | JS    | JS     |

  Scenario Outline: Goertzel filter can detect two SELCAL tones with noise.
    Given the SELCAL tones <tones>
    And a chosen noise level <noise_level>
    And a Goertzel filter tuned for tones <ftones>
    When the tone generation function is run without variations
    Then a sample is generated for the corresponding frequency
    And the sample is fed into the Goertzel filter
    And the Goertzel filter does detect the frequencies.

    Examples:
      | tones | ftones | noise_level |
      | AC    | AC     | 0.20        |
      | BH    | BH     | 2.60        |
      | CK    | CK     | 0.90        |
      | DE    | DE     | 3.10        |
      | EG    | EG     | 1.20        |
      | FP    | FP     | 5.30        |
      | GR    | GR     | 1.40        |
      | HM    | HM     | 0.80        |
      | JQ    | JQ     | 9.20        |
      | KL    | KL     | 3.50        |
      | LS    | LS     | 5.90        |
      | BM    | BM     | 7.30        |
      | DP    | DP     | 0.10        |
      | AQ    | AQ     | 2.40        |
      | FR    | FR     | 1.60        |
      | JS    | JS     | 3.70        |
