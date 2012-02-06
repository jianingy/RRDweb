<%inherit file="/base.mako"/>
<dl>
%if up:
<dt><a href="/${up}">..</a></dt>
%endif
%for entry in entries:
  %if "subitems" in entry:
    <dt>${entry["text"]}</dt>
    %for subitem in entry["subitems"]:
    <dd><a href="${subitem["href"]}">${subitem["text"]}</a></dd>
    %endfor
  %else:
  <dt><a href="${entry["href"]}">${entry["text"]}</a></dt>
  %endif
%endfor
</dl>
