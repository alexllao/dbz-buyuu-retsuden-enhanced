import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import java.util.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

/** Explicit entry seeds from reset/exception vectors and audited native program tables. */
public class SeedSpanishStudy extends GhidraScript {
 private Set<Long> seeds=new TreeSet<>();
 private ArrayList<String> log=new ArrayList<>();
 private void seed(long a,String reason) throws Exception {
  if(a<0x200||a>=0x200000||(a&1)!=0)return;
  if(seeds.add(a)){Address x=toAddr(a);disassemble(x);if(getFunctionAt(x)==null)createFunction(x,null);currentProgram.getSymbolTable().addExternalEntryPoint(x);}
  log.add(String.format("%08x\t%s",a,reason));
 }
 private void program(int id,String reason) throws Exception {
  long table;int index;
  if(id<0x400){table=0x19bce;index=id;}
  else if(id<0x800){table=0x1ccba;index=id-0x400;}
  else if(id<0xc00){table=0x136b6;index=id-0x800;}
  else {table=0x1d028;index=id-0xc00;}
  long entry=table+2*index;long target=entry+getShort(toAddr(entry));
  seed(target,String.format("programa%04x; tabla%08x; %s",id,entry,reason));
 }
 public void run() throws Exception {
  for(int i=1;i<64;i++){long a=Integer.toUnsignedLong(getInt(toAddr(i*4)));seed(a,"vector"+i);}
  // Reset dispatch at420: state is masked byFFFC and indexes branch stubs.
  // State0 waits, while valid states04..38 select these fourteen BRA.W entries.
  for(long a=0x462;a<0x49a;a+=4){if(Short.toUnsignedInt(getShort(toAddr(a)))!=0x6000)throw new Exception("Main-state stub changed");seed(a,"salto_estado_principal_auditado");}
  for(int cid=0;cid<11;cid++) {
   long e=0x2216a+cid*2;long p=e+getShort(toAddr(e));int count=0;
   while(getShort(toAddr(p))>=0&&count<80){program(Short.toUnsignedInt(getShort(toAddr(p+2))),"tabla_tecnicas_CID"+cid);p+=12;count++;}
   if(count>=80)throw new Exception("Unexpected move table length");
  }
  for(int id=0x400;id<0x484;id++)program(id,"11personajes_x12golpes_basicos");
  int[] nativeIds={0,1,2,3,4,5,6,7,8,0x28,0x29,0x2f,0x30,0x31,0x32,0x33,0x34,0x3a,0x3b,0x3c,0x3d,0x51,0x55,0x5a,0x5d,0x61,0x62,0x63,0x65,0x66,0x68,0x69,0x6a,0x6d,0x73,0xa1,0xa4,0xa5,0xa6,0xa7,0xa8,0xc0,0xc1,0xc2,0xe5,0xe6,0x143,0x188};
  for(int id:nativeIds)program(id,"programa_generico_auditado");
  long[] known={0x206,0x8f58,0x8f68,0x9170,0x917c,0x922a,0x9258,0x92b2,0x11c9c,0x124c0,0x13020,0x1631c,0x20b7a,0x20ba0,0x77844,0x77a4c,0x78094};
  for(long a:known)seed(a,"ancla_documentada");
  Path out=Path.of(getScriptArgs()[0]);Files.createDirectories(out);Files.write(out.resolve("seeds.tsv"),log,StandardCharsets.UTF_8);
  println("SPANISH_STUDY_SEEDS unique="+seeds.size()+" references="+log.size()+" noLinearSweep=true");
 }
}
