package ch.securify;

import ch.securify.analysis.SecurifyErrors;

import java.util.HashMap;

public class SolidityResult {
    private static final SolidityResult INSTANCE = new SolidityResult();
    private SolidityResult(){}

    public static SolidityResult getInstance(){
        return INSTANCE;
    }

    HashMap<String, SmallPatternResult> results = new HashMap<>();

    SecurifyErrors securifyErrors = new SecurifyErrors();
}