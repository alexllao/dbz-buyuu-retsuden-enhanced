import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import ghidra.util.NumericUtilities;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

/** Read-only export of existing analysis; never linear-disassembles opaque ROM data. */
public class ExportSpanishStudy extends GhidraScript {
 public void run() throws Exception {
  Path out=Path.of(getScriptArgs()[0]);Files.createDirectories(out);
  long size=0x200000L;int instructions=0,functions=0;
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve("instructions.tsv"),StandardCharsets.UTF_8))) {
   w.println("address\tlength\thex\tassembly\tfunction");
   InstructionIterator it=currentProgram.getListing().getInstructions(true);
   while(it.hasNext()) {
    Instruction i=it.next();long a=i.getAddress().getOffset();
    if(a<0||a+i.getLength()>size)continue;
    Function f=currentProgram.getFunctionManager().getFunctionContaining(i.getAddress());
    w.printf("%08x\t%d\t%s\t%s\t%s%n",a,i.getLength(),NumericUtilities.convertBytesToString(i.getBytes()).replace(" ",""),i.toString().replace('\t',' '),f==null?"":f.getName());instructions++;
   }
  }
  try(PrintWriter w=new PrintWriter(Files.newBufferedWriter(out.resolve("functions.tsv"),StandardCharsets.UTF_8))) {
   w.println("address\tname\tbodyBytes\tranges");
   FunctionIterator it=currentProgram.getFunctionManager().getFunctions(true);
   while(it.hasNext()) {
    Function f=it.next();long a=f.getEntryPoint().getOffset();if(a<0||a>=size)continue;
    StringBuilder rs=new StringBuilder();AddressRangeIterator ranges=f.getBody().getAddressRanges();
    while(ranges.hasNext()){AddressRange r=ranges.next();if(rs.length()>0)rs.append(',');rs.append(String.format("%08x-%08x",r.getMinAddress().getOffset(),r.getMaxAddress().getOffset()));}
    w.printf("%08x\t%s\t%d\t%s%n",a,f.getName(),f.getBody().getNumAddresses(),rs);functions++;
   }
  }
  println("SPANISH_STUDY_EXPORTED instructions="+instructions+" functions="+functions+" noNewDisassembly=true");
 }
}
