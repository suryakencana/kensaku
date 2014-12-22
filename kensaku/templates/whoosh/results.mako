<div class="hits">
    <input type="hidden" name="count" id="count" value="${args.get("count")}" />

    <table class="table">
        <tr>
            <th>Query repr</th><td>${repr(q)}</td>
        </tr>
        <tr>
            <th>Query string</th><td>${unicode(q)}</td>
        </tr>
        <tr>
            <th>Run time</th><td>${"%0.04f" % results.runtime} s</td>
        </tr>
        % if corrected:
        <tr>
##            <th>Did you mean</th><td>${corrected}</td>
        </tr>
        % endif
##        % if results.facet_names():
##            <tr>
##                <th>Groups</th><td>${results.groups("agent_name")}</td>
##            </tr>
##        % endif
    </table>

    <p>Scored ${results.scored_length()} of exactly ${len(results)} results</p>

    % if results:
        <ol>
            %for hit in resultpages:
                <li>
                    <a href="${request.route_url('promo', ref_tag=hit["promo_id"], ref_id=hit["packet_id"])}">
                    ${hit["promo_name"]}
                    </a>
                    (${hit["idx"]}) - (${hit["agent_id"]}) :: (${hit["packet_id"]})
                    % if hit.rank < 10:
##                    <p>${hilite(hit)} - hit ::</p>
                    % endif
                </li>
            %endfor
        </ol>
    % endif
</div>


