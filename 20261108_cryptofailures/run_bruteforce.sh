#php -m | grep pcntl
#php brute_crypt.php MA MAQ55hx59Xoc6 MAB0vELZMxT12 MAG95sRn3ShaA MAilFSJfZK0gk MAJVl1hv%2FHiXw MAm4nc9Zug.fE MAyFFy%2F62phtg MAxkvPnEjvwlY MA.b3dMP6Qtn6 MAh10VEOn4QWQ MADH6Yr2eiR9Q MA6iZ.gHAlFtE MA5ehYo22HShU MA64rWOnfxdDs MASdhoaQhzY7I MApsGQbC3Wphk MApRdg.dVlGgc MA5CKIyPZlSiQ MAV9TKiJ2FljY MAfOJJxXj6I4Q MAZB4Ldc7h2pc MAxdwcrBVTgss MAfYNDmDRgINU MA1wwPjDL9BY. MAuWvzzAWfLWQ MAAxTsDcFt4aQ MAzKvfPzj2GXw MAUXbdyjPpwMI MAFr2sN558Oow MALglWua%2FbKnY MAfUUxNZAT4Ao MANmz1hp3QddE MA8yhKYOvo0Kk MAiiFr9J6yXrE

#hashcat -m 1500 -a 3 hashes.txt ?d?l?u?s?d?l?u?s
# hashcat -m 1500 -a 3 -w 1 \
#     -d 1 \
#     hashes.txt \
#     ?1?1?1?1?1?1?1?1 \
#     -1 "0-9a-zA-Z_{}"

#hashcat -m 1500 -w 1 -a 3 hashes.txt ?1?1?1?1?1?1?1?1 -1 "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"

hashcat -m 1500 -a 3 hashes.txt -1 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ?1?1?1?1?1?1?1?1 --increment

# hashcat -m 1500 -a 3 hashes.txt -1 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ?1?1?1?1?1?1?1?1 --remove 