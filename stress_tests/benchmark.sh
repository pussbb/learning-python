#!/bin/bash

serve_urls="$(cat <<'EOF'
http://site.com/
http://site.com/website-stress-testing/
http://site.com/disaster-recovery/
http://site.com/proof-of-concept/
http://site.com/it-consulting/
http://site.com/project-environments/
EOF
)"

for i in $serve_urls; do
    echo "$i"
    ab -n 2000 -c 1020 -r -q $i &
done

post_lua=$(mktemp /tmp/post-dataXXXXXX.lua)
cat <<EOF >> $post_lua

wrk.method = "POST"
pdf_files = {}
redirects_count = 0
counter_downloads= 0
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"

request = function()
   file = table.remove(pdf_files,1)
   if not file then
        counter = math.random (5949494949494)
        body=string.format("formBuilderForm[FormBuilderID]=1&formBuilderForm[First_name]=test%d&formBuilderForm[Last_Name]=test%d&formBuilderForm[Email]=test%d@madeit%d.com&formBuilderForm[phone]=94585454854854&formBuilderForm[City]=TestCity&formBuilderForm[Country]=0&formBuilderForm[Company_Name]=TestCompany&formBuilderForm[Job_Title]=Test job&formBuilderForm[Explicit_Consent]=just a test&REFERER=&PAGE=http://site.com/test-pdf-download/", counter, counter, counter, counter)
        return wrk.format(nil, nil, nil, body)
   else
        counter_downloads = counter_downloads + 1
        return wrk.format('GET', file)
   end
end

function delay()
   return math.random(1, 2)
end

function response(status, headers, body)
   ---require 'pl.pretty'.dump(status)
   --require 'pl.pretty'.dump(headers)
   ---require 'pl.pretty'.dump(body)
   --- require 'pl.pretty'.dump()
   if status == 302 then
        ---io.write(string.format("%s\n", headers['Location']))
        redirects_count = redirects_count + 1
        pdf_files[#pdf_files + 1] = headers['Location']
   end
   
   --io.write(string.format("%s\n", headers['Location']))
end

function done(summary, latency, requests)
    ----require 'pl.pretty'.dump(summary)
    
    --io.write(string.format(" Form redirects count :%d\n", redirects_count))
    --io.write(string.format(" Started downloads :%d\n", counter_downloads))
    
    io.write(string.format(" total socket connection errors:%d\n", summary['errors']['connect']))
    io.write(string.format(" total socket read errors:%d\n", summary['errors']['read']))
    io.write(string.format(" total socket write errors:%d\n", summary['errors']['write']))
    io.write(string.format("  total HTTP status codes > 399 :%d\n", summary['errors']['status']))
    io.write(string.format(" total request timeouts:%d\n", summary['errors']['timeout']))
end

EOF


wrk -t40 -c40 -d5m -s $post_lua http://site.com/test-pdf-download/ &
wait
