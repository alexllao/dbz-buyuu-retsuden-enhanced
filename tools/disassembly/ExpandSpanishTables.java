import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.*;

/** Recognize only a concrete native relative-word dispatch idiom, never arbitrary ROM words. */
public class ExpandSpanishTables extends GhidraScript {
 public void run() throws Exception {
  Set<Long> seen=new HashSet<>();ArrayList<String> log=new ArrayList<>();int total=0;
  Pattern lea=Pattern.compile("lea \\(0x([0-9a-f]+),PC,D[0-7][wl]\\*0x1\\),(A[0-7])",Pattern.CASE_INSENSITIVE);
  for(int pass=0;pass<4;pass++) {
   ArrayList<long[]> tables=new ArrayList<>();InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()) {
    Instruction i=it.next();Matcher m=lea.matcher(i.toString());if(!m.matches())continue;
    Instruction j=getInstructionAt(i.getAddress().add(i.getLength()));if(j==null)continue;
    if(j.getMnemonicString().equalsIgnoreCase("nop"))j=getInstructionAt(j.getAddress().add(j.getLength()));
    if(j==null||!j.toString().equalsIgnoreCase("adda.w ("+m.group(2)+"),"+m.group(2)))continue;
    Instruction k=getInstructionAt(j.getAddress().add(j.getLength()));if(k==null)continue;
    if(!k.toString().equalsIgnoreCase("jsr ("+m.group(2)+")")&&!k.toString().equalsIgnoreCase("jmp ("+m.group(2)+")"))continue;
    long table=Long.parseLong(m.group(1),16);if(seen.contains(table))continue;
    int first=getShort(toAddr(table));if(first<2||first>1024||(first&1)!=0)continue;
    int count=first/2;long end=table+first;boolean valid=true;long[] targets=new long[count+2];targets[0]=table;targets[1]=count;
    for(int n=0;n<count;n++) {
     long e=table+n*2;long target=e+getShort(toAddr(e));targets[n+2]=target;
     if(target<end||(target&1)!=0||!(target<0x80000||(target>=0x1ae000&&target<0x1b0000))){valid=false;break;}
     int word=Short.toUnsignedInt(getShort(toAddr(target)));if(word==0xffff){valid=false;break;}
    }
    if(valid){tables.add(targets);seen.add(table);}
   }
   if(tables.isEmpty())break;
   for(long[] t:tables) {
    // The recognized word table is data, even if speculative analysis reached it.
    clearListing(toAddr(t[0]),toAddr(t[0]+t[1]*2-1));
    for(int n=0;n<t[1];n++)createWord(toAddr(t[0]+n*2));
    for(int n=2;n<t.length;n++) {
     disassemble(toAddr(t[n]));if(getFunctionAt(toAddr(t[n]))==null)createFunction(toAddr(t[n]),null);currentProgram.getSymbolTable().addExternalEntryPoint(toAddr(t[n]));total++;
     log.add(String.format("%08x\t%08x\t%d\tLEA(PC,index)+ADDA.W(table)+JSR; positive-first-target-bound",t[0],t[n],pass));
    }
   }
   analyzeChanges(currentProgram);
  }
  Files.write(Path.of(getScriptArgs()[0]).resolve("relative-dispatch-tables.tsv"),log,StandardCharsets.UTF_8);
  println("SPANISH_RELATIVE_TABLES tables="+seen.size()+" targetReferences="+total+" noLinearSweep=true");
 }
}
