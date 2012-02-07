<%inherit file="/base.mako"/>
     <h1>${title}</h1>
     <div><a href="${up.replace("view", "list")}">back</a></div>
     <div id="graph">
       <img src="/graph/${graph}" />
     </div>

     <div id="panel">
       <h2> control panel </h2>
       <form>
         <table>
           <tr>
             <td>
               <label for="ds">Data Sources</label>
               <select multiple size=10 name="ds">
                 %for ds in ds_all:
                 %if ds in ds_selected:
                 <option selected>${ds}</option>
                 %else:
                 <option>${ds}</option>
                 %endif
                 %endfor
               </select>
             </td>
             <td>
               <label for="start_time">Start Time</label>
               <input type="text" name="start_time" value="${start_time}">
               <label for="end_time">End Time</label>
               <input type="text" name="end_time" value="${end_time}">
             </td>
             <td>
               <label for="width">width</label>
               <input type="text" name="width" value="${width}">
               <label for="height">height</label>
               <input type="text" name="height" value="${height}">
             </td>
           <tr>
             <td colspan="3">
               <input type="submit" value="Go">
             </td>
           </tr>
         </table>
       </form>
     </div>
