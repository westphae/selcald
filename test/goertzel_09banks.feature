# Created by eric at 11/12/15
Feature: Goertzel filter passes example tests laid out by Kevin Banks at
  http://www.embedded.com/design/configurable-systems/4024443/The-Goertzel-Algorithm
  (with slight adjustments to the received values to account for the difference
  between his float and our double precision).

  Background: I am set up to receive samples with particular parameters.
    Given a sampling rate 8000 Hz
    And a chunk size of 205

  Scenario Outline: basic Goertzel, three sample frequencies
    Given I have a basic Goertzel filter for target frequency 941 Hz
    When I pass a sample of frequency <sample_freq> through the filter
    Then I get a real value <real>
    And an imaginary value <imag>
    And I get a magnitude squared <m2>
    And a magnitude <m>.

    Examples: Various frequencies
      | sample_freq | real          | imag         | m2               | m            |
      | 691         |  -360.392059  |   -45.871609 |    131986.640625 |   363.299652 |
      | 941         | -3727.528076  | -9286.238281 | 100128688.000000 | 10006.432617 |
      | 1191        |   424.038116  |  -346.308716 |    299738.062500 |   547.483398 |

  Scenario Outline: optimized Goertzel, three sample frequencies
    Given I have an optimized Goertzel filter for target frequency 941 Hz
    When I pass a sample of frequency <sample_freq> through the filter
    Then I get a magnitude squared <m2>
    And a magnitude <m>.

    Examples: Various frequencies
      | sample_freq | m2               | m            |
      | 691         |    131986.640625 |   363.299652 |
      | 941         | 100128688.000000 | 10006.432617 |
      | 1191        |    299738.062500 |   547.483398 |

  Scenario Outline: basic Goertzel, wide range of sample frequencies
    Given I have a basic Goertzel filter for target frequency 941 Hz
    When I pass a sample of frequency <sample_freq> through the filter
    Then I get a magnitude squared <m2>
    And a magnitude <m>.

    Examples: Various frequencies
      | sample_freq | m2              | m           |
      |  641.0      |    146697.87500 |   383.01160 |
      |  656.0      |     63684.62100 |   252.35812 |
      |  671.0      |     96753.92180 |   311.05292 |
      |  686.0      |    166669.90625 |   408.25226 |
      |  701.0      |      5414.02002 |    73.58002 |
      |  716.0      |    258318.37500 |   508.25031 |
      |  731.0      |    178329.68750 |   422.29099 |
      |  746.0      |     71271.88281 |   266.96796 |
      |  761.0      |    437814.90625 |   661.67584 |
      |  776.0      |     81901.81250 |   286.18494 |
      |  791.0      |    468060.31250 |   684.14935 |
      |  806.0      |    623345.56250 |   789.52234 |
      |  821.0      |     18701.58984 |   136.75375 |
      |  836.0      |   1434181.62500 |  1197.57324 |
      |  851.0      |    694211.75000 |   833.19373 |
      |  866.0      |   1120359.50000 |  1058.47034 |
      |  881.0      |   4626623.00000 |  2150.95874 |
      |  896.0      |    160420.43750 |   400.52521 |
      |  911.0      |  19374364.00000 |  4401.63184 |
      |  926.0      |  81229848.00000 |  9012.76074 |
      |  941.0      | 100128688.00000 | 10006.43262 |
      |  956.0      |  43694608.00000 |  6610.18994 |
      |  971.0      |   1793435.75000 |  1339.19226 |
      |  986.0      |   3519388.50000 |  1876.00330 |
      | 1001.0      |   3318844.50000 |  1821.76965 |
      | 1016.0      |     27707.98828 |   166.45717 |
      | 1031.0      |   1749922.62500 |  1322.84644 |
      | 1046.0      |    478859.28125 |   691.99658 |
      | 1061.0      |    284255.81250 |   533.15643 |
      | 1076.0      |    898392.93750 |   947.83594 |
      | 1091.0      |     11303.36035 |   106.31726 |
      | 1106.0      |    420975.65625 |   648.82635 |
      | 1121.0      |    325753.78125 |   570.74841 |
      | 1136.0      |     36595.78906 |   191.30026 |
      | 1151.0      |    410926.06250 |   641.03516 |
      | 1166.0      |     45246.58594 |   212.71245 |
      | 1181.0      |    119967.59375 |   346.36337 |
      | 1196.0      |    250361.39062 |   500.36127 |
      | 1211.0      |      1758.44263 |    41.93379 |
      | 1226.0      |    190195.57812 |   436.11417 |
      | 1241.0      |     74192.23438 |   272.38251 |
