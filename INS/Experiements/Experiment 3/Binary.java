public class Binary {
    public static String convertTextToBinaryString(String text) { String binaryString = "";
        for (char c : text.toCharArray()) binaryString += Integer.toBinaryString(c);
        return binaryString;
    }

    public static String convertBinaryStringToText(String binaryString){
        String text = "";
        String[] bytes = binaryString.split("(?<=\\G.{7})"); for (String textByte : bytes) text += (char)
        Integer.parseInt(textByte, 2);
        return text;
    }

    public static char XOR(char a, char b) { if (a == b) return '0';
        else return '1';
    }

    public static char maxBit(char a, char b) {
        return a > b ? a : b;
    }


}
