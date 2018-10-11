package ch.securify;

import ch.securify.analysis.SecurifyErrors;

import java.util.HashMap;

public class SolidityResult {
    HashMap<String, SmallPatternResult> results = new HashMap<>();

    SecurifyErrors securifyErrors = null;
}
