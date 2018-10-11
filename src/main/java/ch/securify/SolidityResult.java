package ch.securify;

import ch.securify.analysis.SecurifyError;

import java.util.HashMap;

public class SolidityResult {
    HashMap<String, SmallPatternResult> results = new HashMap<>();

    SecurifyError securifyError = null;
}
