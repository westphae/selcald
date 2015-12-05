# Created by eric at 12/4/15
Feature: channel_monitor detects when its tone is sounded.

  Scenario Outline: Random SELCAL tones are played with noise and
  channel_monitor correctly identifies when its tuned tone is played.
    Given a source with noise <noise> playing random SELCAL tones for 99 seconds
    And a channel monitor tuned for tone <ftone> with sensitivity <sen>
    When the source is fed into the channel monitor
    Then the channel monitor correctly detects the tones.

    Examples:
      | ftone | noise | sen  |
      | A     | 3.5   |  2.5 |
      | B     | 2.2   |  2.5 |
      | C     | 1.6   |  2.5 |
      | D     | 0.7   |  2.5 |
      | E     | 1.1   |  2.5 |
      | F     | 0.5   |  2.5 |
      | G     | 0.9   |  2.5 |
      | H     | 2.4   |  2.5 |
      | J     | 1.3   |  2.5 |
      | K     | 1.6   |  2.5 |
      | L     | 2.6   |  2.5 |
      | M     | 0.0   |  2.5 |
      | P     | 0.1   |  2.5 |
      | Q     | 0.3   |  2.5 |
      | R     | 1.7   |  2.5 |
      | S     | 0.6   |  2.5 |
      | A     | 3.5   |  4.0 |
      | B     | 2.2   |  4.0 |
      | C     | 1.6   |  4.0 |
      | D     | 0.7   |  4.0 |
      | E     | 1.1   |  4.0 |
      | F     | 0.5   |  4.0 |
      | G     | 0.9   |  4.0 |
      | H     | 2.4   |  4.0 |
      | J     | 1.3   |  4.0 |
      | K     | 1.6   |  4.0 |
      | L     | 2.6   |  4.0 |
      | M     | 0.0   |  4.0 |
      | P     | 0.1   |  4.0 |
      | Q     | 0.3   |  4.0 |
      | R     | 1.7   |  4.0 |
      | S     | 0.6   |  4.0 |
      | A     | 3.5   |  5.0 |
      | B     | 2.2   |  5.0 |
      | C     | 1.6   |  5.0 |
      | D     | 0.7   |  5.0 |
      | E     | 1.1   |  5.0 |
      | F     | 0.5   |  5.0 |
      | G     | 0.9   |  5.0 |
      | H     | 2.4   |  5.0 |
      | J     | 1.3   |  5.0 |
      | K     | 1.6   |  5.0 |
      | L     | 2.6   |  5.0 |
      | M     | 0.0   |  5.0 |
      | P     | 0.1   |  5.0 |
      | Q     | 0.3   |  5.0 |
      | R     | 1.7   |  5.0 |
      | S     | 0.6   |  5.0 |
      | A     | 3.5   |  6.0 |
      | B     | 2.2   |  6.0 |
      | C     | 1.6   |  6.0 |
      | D     | 0.7   |  6.0 |
      | E     | 1.1   |  6.0 |
      | F     | 0.5   |  6.0 |
      | G     | 0.9   |  6.0 |
      | H     | 2.4   |  6.0 |
      | J     | 1.3   |  6.0 |
      | K     | 1.6   |  6.0 |
      | L     | 2.6   |  6.0 |
      | M     | 0.0   |  6.0 |
      | P     | 0.1   |  6.0 |
      | Q     | 0.3   |  6.0 |
      | R     | 1.7   |  6.0 |
      | S     | 0.6   |  6.0 |


