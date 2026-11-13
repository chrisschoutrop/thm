# Reversing ELF
## Room for beginner Reverse Engineering CTF players
Difficulty: Easy
URL: https://tryhackme.com/room/reverselfiles

### Info given

### Tasks
- Crackme1: What is the flag?
- Crackme2: What is the super secret password ?
- Crackme2: What is the flag?
- Crackme3: What is the flag?
- Crackme4: What is the password ?; Analyze and find the password for the binary?
- Crackme5: What is the input ?; What will be the input of the file to get output Good game ?
- Crackme6: What is the password ?;Analyze the binary for the easy password
- Crackme7: What is the flag ?;Analyze the binary to get the flag
- Crackme8: What is the flag ?;Analyze the binary to get the flag

![alt text](IMAGE.png "Title")

# Content

## Crackme 1
```
$ ./crackme1 
flag{not_that_kind_of_elf}
```

## Crackme 2
```
$ ./crackme2 1234
Access denied.
```
Flag staat niet bij `strings`\
```c

undefined4 main(int param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  int iVar2;
  
  if (param_1 == 2) {
    iVar2 = strcmp((char *)param_2[1],"super_secret_password");
    if (iVar2 == 0) {
      puts("Access granted.");
      giveFlag();
      uVar1 = 0;
    }
    else {
      puts("Access denied.");
      uVar1 = 1;
    }
  }
  else {
    printf("Usage: %s password\n",*param_2);
    uVar1 = 1;
  }
  return uVar1;
}
```
Password: `super_secret_password`
Flag: `flag{if_i_submit_this_flag_then_i_will_get_points}`

## Crackme 3

Main function is given by:
```c
undefined4 FUN_080484f4(int param_1,undefined4 *param_2)

{
  char *__s;
  size_t sVar1;
  char *__s_00;
  int iVar2;
  
  if (param_1 == 2) {
    __s = (char *)param_2[1];
    sVar1 = strlen(__s);
    __s_00 = malloc(sVar1 * 2);
    if (__s_00 == (char *)0x0) {
      fwrite("malloc failed\n",0xe,1,stderr);
    }
    else {
      sVar1 = strlen(__s);
      FUN_080486b0(__s,__s_00,sVar1,0);
      sVar1 = strlen(__s_00);
      if ((sVar1 == 0x40) &&
         (iVar2 = strcmp(__s_00,"ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ=="),
         iVar2 == 0)) {
        puts("Correct password!");
        return 0;
      }
      puts("Come on, even my aunt Mildred got this one!");
    }
  }
  else {
    fprintf(stderr,"Usage: %s PASSWORD\n",*param_2);
  }
  return 0xffffffff;
}
```
Dit lijkt base64: `ZjByX3kwdXJfNWVjMG5kX2xlNTVvbl91bmJhc2U2NF80bGxfN2gzXzdoMW5nNQ==`
`f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5`

```
$ ./crackme3 f0r_y0ur_5ec0nd_le55on_unbase64_4ll_7h3_7h1ng5
Correct password!
```

## Crackme 4
```c

undefined8 main(int param_1,undefined8 *param_2)

{
  if (param_1 == 2) {
    compare_pwd(param_2[1]);
  }
  else {
    printf("Usage : %s password\nThis time the string is hidden and we used strcmp\n",*param_2);
  }
  return 0;
}
```
```c
void compare_pwd(char *param_1)

{
  int iVar1;
  long in_FS_OFFSET;
  char local_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  builtin_strncpy(local_28,"I]{I\x14V\x17{WAGQV\x17{TS@",0x13);
  get_pwd(local_28);
  iVar1 = strcmp(local_28,param_1);
  if (iVar1 == 0) {
    puts("password OK");
  }
  else {
    printf("password \"%s\" not OK\n",param_1);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
Dit mysterie gaat `get_pwd` in: `I]{I\x14V\x17{WAGQV\x17{TS@` en wordt vergeleken met het password.
```c
void get_pwd(long param_1)

{
  undefined4 local_c;
  
  local_c = -1;
  while (local_c = local_c + 1, *(char *)(param_1 + local_c) != '\0') {
    *(byte *)(local_c + param_1) = *(byte *)(param_1 + local_c) ^ 0x24;
  }
  return;
}
```
Cleanup:
```c
void get_pwd(char *encoded_password)

{
  int index;
  
  index = -1;
  while (index = index + 1, encoded_password[index] != '\0') {
    encoded_password[index] = encoded_password[index] ^ 0x24;
  }
  return;
}
```
Dus het XOR't het mysterie met 0x24. XOR is zijn eigen inverse, dus mysterie XOR 0x24 levert het password op, dat kan met cyberchef.
Password: `my_m0r3_secur3_pwd`

## Crackme 5
```c

undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  undefined1 local_58 [32];
  undefined1 local_38;
  undefined1 local_37;
  undefined1 local_36;
  undefined1 local_35;
  undefined1 local_34;
  undefined1 local_33;
  undefined1 local_32;
  undefined1 local_31;
  undefined1 local_30;
  undefined1 local_2f;
  undefined1 local_2e;
  undefined1 local_2d;
  undefined1 local_2c;
  undefined1 local_2b;
  undefined1 local_2a;
  undefined1 local_29;
  undefined1 local_28;
  undefined1 local_27;
  undefined1 local_26;
  undefined1 local_25;
  undefined1 local_24;
  undefined1 local_23;
  undefined1 local_22;
  undefined1 local_21;
  undefined1 local_20;
  undefined1 local_1f;
  undefined1 local_1e;
  undefined1 local_1d;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_38 = 0x4f;
  local_37 = 0x66;
  local_36 = 100;
  local_35 = 0x6c;
  local_34 = 0x44;
  local_33 = 0x53;
  local_32 = 0x41;
  local_31 = 0x7c;
  local_30 = 0x33;
  local_2f = 0x74;
  local_2e = 0x58;
  local_2d = 0x62;
  local_2c = 0x33;
  local_2b = 0x32;
  local_2a = 0x7e;
  local_29 = 0x58;
  local_28 = 0x33;
  local_27 = 0x74;
  local_26 = 0x58;
  local_25 = 0x40;
  local_24 = 0x73;
  local_23 = 0x58;
  local_22 = 0x60;
  local_21 = 0x34;
  local_20 = 0x74;
  local_1f = 0x58;
  local_1e = 0x74;
  local_1d = 0x7a;
  puts("Enter your input:");
  __isoc99_scanf(&DAT_00400966,local_58);
  iVar1 = strcmp_(local_58,&local_38);
  if (iVar1 == 0) {
    puts("Good game");
  }
  else {
    puts("Always dig deeper");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
Komt er wat uit als we al die hex waardes achter elkaar zetten en decoden?
```
$ ./crackme5
Enter your input:
OfdlDSA|3tXb32~X3tX@sX`4tXtz
Good game
```
Password: OfdlDSA|3tXb32~X3tX@sX`4tXtz

## Crackme 6
```c

undefined8 main(int param_1,undefined8 *param_2)

{
  if (param_1 == 2) {
    compare_pwd(param_2[1]);
  }
  else {
    printf("Usage : %s password\nGood luck, read the source\n",*param_2);
  }
  return 0;
}
```
```c
void compare_pwd(undefined8 param_1)

{
  int iVar1;
  
  iVar1 = my_secure_test(param_1);
  if (iVar1 == 0) {
    puts("password OK");
  }
  else {
    printf("password \"%s\" not OK\n",param_1);
  }
  return;
}
```
```c

undefined8 my_secure_test(char *param_1)

{
  undefined8 uVar1;
  
  if ((*param_1 == '\0') || (*param_1 != '1')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[1] == '\0') || (param_1[1] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[2] == '\0') || (param_1[2] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[3] == '\0') || (param_1[3] != '7')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[4] == '\0') || (param_1[4] != '_')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[5] == '\0') || (param_1[5] != 'p')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[6] == '\0') || (param_1[6] != 'w')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[7] == '\0') || (param_1[7] != 'd')) {
    uVar1 = 0xffffffff;
  }
  else if (param_1[8] == '\0') {
    uVar1 = 0;
  }
  else {
    uVar1 = 0xffffffff;
  }
  return uVar1;
}
```
```
$ ./crackme6 1337_pwd
password OK
```
Password: `1337_pwd`

## Crackme 7
```c

undefined4 main(void)

{
  int iVar1;
  undefined4 *puVar2;
  byte bVar3;
  undefined4 local_80 [25];
  int local_1c;
  int local_18;
  int local_14;
  undefined1 *local_10;
  
  bVar3 = 0;
  local_10 = &stack0x00000004;
  while( true ) {
    while( true ) {
      puts("Menu:\n\n[1] Say hello\n[2] Add numbers\n[3] Quit");
      printf("\n[>] ");
      iVar1 = __isoc99_scanf(&DAT_08048814,&local_14);
      if (iVar1 != 1) {
        puts("Unknown input!");
        return 1;
      }
      if (local_14 != 1) break;
      printf("What is your name? ");
      puVar2 = local_80;
      for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar2 = 0;
        puVar2 = puVar2 + (uint)bVar3 * -2 + 1;
      }
      iVar1 = __isoc99_scanf(&DAT_0804883a,local_80);
      if (iVar1 != 1) {
        puts("Unable to read name!");
        return 1;
      }
      printf("Hello, %s!\n",local_80);
    }
    if (local_14 != 2) {
      if (local_14 == 3) {
        puts("Goodbye!");
      }
      else if (local_14 == 0x7a69) {
        puts("Wow such h4x0r!");
        giveFlag();
      }
      else {
        printf("Unknown choice: %d\n",local_14);
      }
      return 0;
    }
    printf("Enter first number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_18);
    if (iVar1 != 1) break;
    printf("Enter second number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_1c);
    if (iVar1 != 1) {
      puts("Unable to read number!");
      return 1;
    }
    printf("%d + %d = %d\n",local_18,local_1c,local_18 + local_1c);
  }
  puts("Unable to read number!");
  return 1;
}
```
Cleanup:
```c

undefined4 main(void)

{
  int iVar1;
  undefined4 *puVar2;
  byte bVar3;
  undefined4 local_80 [25];
  int local_1c;
  int local_18;
  int target;
  undefined1 *local_10;
  
  bVar3 = 0;
  local_10 = &stack0x00000004;
  while( true ) {
    while( true ) {
      puts("Menu:\n\n[1] Say hello\n[2] Add numbers\n[3] Quit");
      printf("\n[>] ");
      iVar1 = __isoc99_scanf(&Procentu,&target);
      if (iVar1 != 1) {
        puts("Unknown input!");
        return 1;
      }
      if (target != 1) break;
      printf("What is your name? ");
      puVar2 = local_80;
      for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar2 = 0;
        puVar2 = puVar2 + (uint)bVar3 * -2 + 1;
      }
      iVar1 = __isoc99_scanf(&Procent99s,local_80);
      if (iVar1 != 1) {
        puts("Unable to read name!");
        return 1;
      }
      printf("Hello, %s!\n",local_80);
    }
    if (target != 2) {
      if (target == 3) {
        puts("Goodbye!");
      }
      else if (target == 31337) {
        puts("Wow such h4x0r!");
        giveFlag();
      }
      else {
        printf("Unknown choice: %d\n",target);
      }
      return 0;
    }
    printf("Enter first number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_18);
    if (iVar1 != 1) break;
    printf("Enter second number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_1c);
    if (iVar1 != 1) {
      puts("Unable to read number!");
      return 1;
    }
    printf("%d + %d = %d\n",local_18,local_1c,local_18 + local_1c);
  }
  puts("Unable to read number!");
  return 1;
}
```
```c
void giveFlag(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *puVar3;
  char local_ca [34];
  undefined4 local_a8 [34];
  uint local_20;
  
  puVar2 = &DAT_080488e0;
  puVar3 = local_a8;
  for (iVar1 = 0x22; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *puVar2;
    puVar2 = puVar2 + 1;
    puVar3 = puVar3 + 1;
  }
  memset(local_ca,0x41,0x22);
  for (local_20 = 0; local_20 < 0x22; local_20 = local_20 + 1) {
    local_ca[local_20] = (char)local_a8[local_20] + local_ca[local_20];
  }
  puts(local_ca);
  return;
}
```
Cleanup:
```c

void giveFlag(void)

{
  int iVar1;
  char *puVar2;
  char *puVar3;
  char output_buffer [34];
  char input_buffer [136];
  uint index;
  
  puVar2 = "%";
  puVar3 = input_buffer;
  for (iVar1 = 34; iVar1 != 0; iVar1 = iVar1 + -1) {
    *(undefined4 *)puVar3 = *(undefined4 *)puVar2;
    puVar2 = puVar2 + 4;
    puVar3 = puVar3 + 4;
  }
  memset(output_buffer,0x41,34);
  for (index = 0; index < 34; index = index + 1) {
    output_buffer[index] = (char)*(undefined4 *)(input_buffer + index * 4) + output_buffer[index];
  }
  puts(output_buffer);
  return;
}
```
Volgens mij kom ik daar uiteindelijk wel uit, maar het lijkt te complex voor deze challenge gegeven dat de rest vrij triviaal was.
```c
$ ./crackme7
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 31337
Wow such h4x0r!
flag{much_reversing_very_ida_wow}
```
Ik had `31137` getypt ipv `31337` oeps.
Flag: `flag{much_reversing_very_ida_wow}`

## Crackme 8
```c
undefined4 main(int param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  int iVar2;
  
  if (param_1 == 2) {
    iVar2 = atoi((char *)param_2[1]);
    if (iVar2 == -0x35010ff3) {
      puts("Access granted.");
      giveFlag();
      uVar1 = 0;
    }
    else {
      puts("Access denied.");
      uVar1 = 1;
    }
  }
  else {
    printf("Usage: %s password\n",*param_2);
    uVar1 = 1;
  }
  return uVar1;
}
```
-0x35010ff3=-889262067
```
$ ./crackme8 -889262067
Access granted.
flag{at_least_this_cafe_wont_leak_your_credit_card_numbers}
```
FLAG: flag{at_least_this_cafe_wont_leak_your_credit_card_numbers}