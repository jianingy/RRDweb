<%inherit file="/base.mako"/>
<form>
    <table>
        <tr>
            <td>
                <%
                if hostname:
                  readonly = "readonly"
                else:
                  readonly = ""
                %>
                <label>Hostname:</label> <input name="hostname" type="text" value="${hostname}" ${readonly}>
            </td>
            <td>
                %if items:
                <label>RRD:</label>
                <select name="filename">
                    %for item in items:
                    <option value="${item}">${item}</option>
                    %endfor
                </select>
                %endif
            </td>
            <tr>
                <td><input type="submit" value="Go!">
                    <a href="/remote">Back!</a></td>
            </tr>
        </tr>
    </table>
</form>
