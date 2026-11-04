import ghidra.app.script.GhidraScript;
import ghidra.app.plugin.assembler.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;
import java.io.*;

public class AssembleAura extends GhidraScript {
 public void run() throws Exception {
  String[] args=getScriptArgs();
  List<String> lines=Files.readAllLines(Path.of(args[0]),StandardCharsets.UTF_8);
  Assembler assembler=Assemblers.getAssembler(currentProgram);
  Map<String,Long> labels=new LinkedHashMap<>();
  long base=0x7b400,pc=base;
  ByteArrayOutputStream bytes=new ByteArrayOutputStream();
  ArrayList<String> listing=new ArrayList<>();
  Pattern symbol=Pattern.compile("@([a-zA-Z0-9_]+)");
  for(int pass=0;pass<2;pass++) {
   pc=base;bytes.reset();listing.clear();
   for(String raw:lines) {
    String line=raw.split(";",2)[0].trim();
    if(line.isEmpty())continue;
    if(line.endsWith(":")){labels.put(line.substring(0,line.length()-1),pc);continue;}
    Matcher matcher=symbol.matcher(line);StringBuffer rendered=new StringBuffer();
    while(matcher.find())matcher.appendReplacement(rendered,"0x"+Long.toHexString(labels.getOrDefault(matcher.group(1),pc+16)));
    matcher.appendTail(rendered);line=rendered.toString();
    Matcher shorts=Pattern.compile("\\(0xffff([0-9a-fA-F]{4})\\)\\.w").matcher(line);
    StringBuffer fixed=new StringBuffer();
    while(shorts.find())shorts.appendReplacement(fixed,"(-0x"+Integer.toHexString(0x10000-Integer.parseInt(shorts.group(1),16))+").w");
    shorts.appendTail(fixed);line=fixed.toString();
    String opcode=line.split(" ",2)[0];
    if(opcode.equals("moveq"))line=line.replace("moveq #","moveq ");
    int bits=opcode.endsWith(".b")?8:opcode.endsWith(".w")?16:32;
    Matcher imms=Pattern.compile("#0x([0-9a-fA-F]+)").matcher(line);
    StringBuffer signed=new StringBuffer();
    while(imms.find()) {
     long value=Long.parseLong(imms.group(1),16),limit=1L<<(bits-1);
     String token=value>=limit && value<(1L<<bits)?"#-0x"+Long.toHexString((1L<<bits)-value):imms.group();
     imms.appendReplacement(signed,token);
    }
    imms.appendTail(signed);line=signed.toString();
    if(opcode.endsWith(".b"))line=line.replaceAll("\\bD([0-7])\\b","D$1b");
    if(opcode.endsWith(".w") && !opcode.startsWith("mulu") && !opcode.startsWith("divu"))line=line.replaceAll("\\bD([0-7])\\b","D$1w");
    byte[] code;
    if(line.startsWith(".hex "))code=HexFormat.of().parseHex(line.substring(5).replace(" ",""));
    else {
     try {code=assembler.assembleLine(toAddr(pc),line);}
     catch(Exception e){throw new Exception("At "+Long.toHexString(pc)+" line: "+line,e);}
    }
    listing.add(String.format("%08x: %-40s %s",pc,HexFormat.of().formatHex(code),line));
    bytes.write(code);pc+=code.length;
   }
  }
  Files.write(Path.of(args[1]+".bin"),bytes.toByteArray());
  Files.write(Path.of(args[1]+".listing.txt"),listing,StandardCharsets.UTF_8);
  ArrayList<String> names=new ArrayList<>();for(var e:labels.entrySet())names.add(e.getKey()+"="+Long.toHexString(e.getValue()));
  Files.write(Path.of(args[1]+".labels.txt"),names,StandardCharsets.UTF_8);
  println("CONTROL_PATCH_ASSEMBLED bytes="+bytes.size()+" labels="+labels.size());
 }
}

